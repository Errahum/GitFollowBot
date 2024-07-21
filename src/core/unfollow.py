import time
from src.utils.logger import logger
import requests


class GitHubClientUnfollow:
    def __init__(self, config, username):
        self.token = config.get_api_key()
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.username = username


    def get_following(self):
        return self._get_paginated_data(f'https://api.github.com/users/{self.username}/following')

    def get_followers(self):
        return self._get_paginated_data(f'https://api.github.com/users/{self.username}/followers')

    def _get_paginated_data(self, url):
        page = 1
        data = []
        while True:
            paginated_url = f'{url}?page={page}'
            response = self._make_request_unfollow('GET', paginated_url)

            if response.status_code != 200:
                raise Exception(f"Error fetching data from {paginated_url}. Status code: {response.status_code}")

            page_data = response.json()
            if not page_data:
                break  # No more data to fetch

            data.extend(page_data)
            page += 1

        return data

    def _make_request_unfollow(self, method, url):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=self.headers)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=self.headers)
                else:
                    raise ValueError("Unsupported HTTP method")

                if response.status_code == 500:
                    logger.error(f"Server error (500) at {url}, retrying...")
                    time.sleep(2)  # Wait before retrying
                    continue  # Retry the request

                return response
            except requests.RequestException as e:
                logger.error(f"Request to {url} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retrying
                    continue  # Retry the request
                else:
                    raise


class UnfollowNonFollowers:
    def __init__(self, client, username):
        self.client = client
        self.username = username

    def unfollow_non_followers(self, max_peoples_unfollow):
        following = self.client.get_following()
        followers = self.client.get_followers()

        follower_set = {user['login'] for user in followers}
        unfollow_count = 0
        unfollow_limit = max_peoples_unfollow

        for user in following:
            if user['login'] not in follower_set:
                unfollow_url = f'https://api.github.com/user/following/{user["login"]}'
                response = self.client._make_request_unfollow('DELETE', unfollow_url)

                if response.status_code == 204:
                    logger.info(f"Successfully unfollowed {user['login']}")
                    unfollow_count += 1
                else:
                    logger.error(f"Failed to unfollow {user['login']} with status code {response.status_code}")

                if unfollow_count >= unfollow_limit:
                    logger.warning(f"Reached the unfollow limit of {max_peoples_unfollow} users")
                    break
