from src.follow import GitHubClientFollow, FollowerManager, extract_username_from_url
from src.unfollow import UnfollowNonFollowers, GitHubClientUnfollow

class MainFollowUnfollow:
    def __init__(self, config):
        self.github_client_follow = GitHubClientFollow(config)
        self.github_client_unfollow = GitHubClientUnfollow(config)

    def follow_people(self):
        profile_url = input("Enter the GitHub profile URL: ")
        max_peoples_follow = int(input("Enter the maximum number of people to follow: "))
        try:
            target_username = extract_username_from_url(profile_url)
        except ValueError as e:
            print(e)
            return

        followers = self.github_client_follow.get_followers(target_username)
        following = self.github_client_follow.get_following(target_username)

        follower_manager = FollowerManager(self.github_client_follow, max_peoples_follow)
        valid_users = follower_manager.select_valid_users(followers, following)

        if valid_users:
            follower_manager.follow_users(valid_users)
        else:
            print("No valid users found based on the criteria.")

        print("Process complete.")

    def unfollow_people(self):
        username = input("Enter your GitHub username: ")
        max_peoples_follow = int(input("Enter the maximum number of people to unfollow: "))

        unfollow_manager = UnfollowNonFollowers(self.github_client_unfollow, username, max_peoples_follow)
        unfollow_manager.unfollow_non_followers()

        print("Process complete.")
