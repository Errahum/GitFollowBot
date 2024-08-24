import json

from src.core.follow.follow import GitHubClientFollow, FollowerManager, extract_username_from_url
from src.core.follow.follow_back import GitHubClientFollowBack, FollowBackFollowers
from src.core.follow.get_following import GitHubClientGetFollowings
from src.core.undo.unfollow import UnfollowBot, GitHubClientUnfollow
from src.utils.logger import logger
from src.core.scraper.linkedin import GitHubLinkedInScraper
from src.core.scraper.x import XScraper
from src.core.undo.unstar import GitHubClientUnstar


class MainFollowUnfollow:
    def __init__(self, config):
        get_username = GitHubClientGetFollowings(config)
        self.auth_user = get_username._get_authenticated_user()
        self.username = self.auth_user.get('login')

        self.github_client_follow = GitHubClientFollow(config)
        self.github_client_unfollow = GitHubClientUnfollow(config, self.username)
        self.github_client_get_following = GitHubClientGetFollowings(config)
        self.github_client_follow_back = GitHubClientFollowBack(config)
        self.github_client_unfollow = UnfollowBot(self.github_client_unfollow, self.username)
        self.linkedin_scraper = GitHubLinkedInScraper(config, max_accounts=0)
        self.x_scraper = XScraper(config, max_accounts=0)
        self.GitHubClientUnstar = GitHubClientUnstar(config, self.username)

    def follow_people(self):
        profile_url = input("Enter the GitHub profile URL: ")
        max_peoples_follow = int(input("Enter the maximum number of people to follow: "))
        condition_follow = False
        target_username = None
        jsonl_file = None

        try:
            followings = self.github_client_get_following.get_following()
            jsonl_file = "followings.jsonl"

            with open(jsonl_file, 'w') as f:
                for following in followings:
                    json.dump(following['login'], f)
                    f.write('\n')

            try:
                target_username = extract_username_from_url(profile_url)
            except ValueError as e:
                logger.error(e)
                return
        except Exception as e:
            logger.error(f"GitHub username error {e}")

        followers = self.github_client_follow.get_followers(target_username)
        following = self.github_client_follow.get_following(target_username)

        follower_manager = FollowerManager(self.github_client_follow, max_peoples_follow, jsonl_file)
        valid_users = follower_manager.select_valid_users(followers, following, condition_follow)

        if valid_users:
            follower_manager.follow_users(valid_users)
        else:
            logger.warning("No valid users found based on the criteria.")

        logger.info("Process complete.")

    def unfollow_people(self):

        max_peoples_follow = int(input("Enter the maximum number of people to unfollow: "))

        use_follow_users_list = False
        condition_input_unfollow = input("Enter 't' or 'f' for restrictive conditions: ").strip().lower()

        if condition_input_unfollow == 't':
            use_follow_users_list = True
        elif condition_input_unfollow == 'f':
            use_follow_users_list = False

        unfollow_manager = self.github_client_unfollow
        unfollow_manager.unfollow_non_followers(max_peoples_follow, use_follow_users_list)

        logger.info("Process complete.")

    def follow_back(self):
        condition_input = input("Enter 't' or 'f' for 2min loop: ").strip().lower()
        follow_back_bot = FollowBackFollowers(self.github_client_follow_back, self.username)
        if condition_input == 't':
            follow_back_bot.follow_back_periodically()
        elif condition_input == 'f':
            follow_back_bot.follow_back()

    def linkedin_profiles(self):
        max_accounts = int(input("Enter the maximum number of linkedin account: "))
        if max_accounts <= 0:
            logger.error("Invalid number of accounts.")
        else:
            followers = self.linkedin_scraper.get_github_followers(self.username, max_accounts)
            self.linkedin_scraper.scrape_linkedin_profiles(followers)

    def x_profiles(self):
        max_accounts = int(input("Enter the maximum number of X accounts: "))
        if max_accounts <= 0:
            logger.error("Invalid number of accounts.")
        else:
            followers = self.x_scraper.get_github_followers(self.username, max_accounts)
            self.x_scraper.scrape_X_profiles(followers)

    def unstar_non_followers_repos(self):
        self.GitHubClientUnstar.unstar_non_followers_repos()
        logger.info("Unstar process complete.")
