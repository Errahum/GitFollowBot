import json

from src.core.follow import GitHubClientFollow, FollowerManager, extract_username_from_url
from src.core.follow_back import GitHubClientFollowBack, FollowBackFollowers
from src.core.get_following import GitHubClientGetFollowings
from src.core.unfollow import UnfollowNonFollowers, GitHubClientUnfollow
from src.utils.logger import logger

class MainFollowUnfollow:
    def __init__(self, config):
        get_username = GitHubClientGetFollowings(config)
        self.auth_user = get_username._get_authenticated_user()
        self.username = self.auth_user.get('login')

        self.github_client_follow = GitHubClientFollow(config)
        self.github_client_unfollow = GitHubClientUnfollow(config, self.username)
        self.github_client_get_following = GitHubClientGetFollowings(config)
        self.github_client_follow_back = GitHubClientFollowBack(config)
        self.github_client_unfollow_not_follow = UnfollowNonFollowers(self.github_client_unfollow, self.username)

    def follow_people(self):
        profile_url = input("Enter the GitHub profile URL: ")
        max_peoples_follow = int(input("Enter the maximum number of people to follow: "))
        condition_follow = False
        condition_input = input("Enter 't' or 'f' for restrictive conditions: ").strip().lower()
        target_username = None
        jsonl_file = None

        if condition_input == 't':
            condition_follow = True
        elif condition_input == 'f':
            condition_follow = False

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

        unfollow_manager = self.github_client_unfollow_not_follow
        unfollow_manager.unfollow_non_followers(max_peoples_follow)

        logger.info("Process complete.")

    def follow_back(self):
        condition_input = input("Enter 't' or 'f' for 2min loop: ").strip().lower()
        follow_back_bot = FollowBackFollowers(self.github_client_follow_back, self.username)
        if condition_input == 't':
            follow_back_bot.follow_back_periodically()
        elif condition_input == 'f':
            follow_back_bot.follow_back()


