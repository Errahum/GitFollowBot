import time
import requests
from src.utils.logger import logger

class GitHubClientFollowBack:
    def __init__(self, config):
        self.token = config.get_api_key()
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_followers(self, username):
        return self._get_paginated_data(f'https://api.github.com/users/{username}/followers')

    def get_following(self, username):
        return self._get_paginated_data(f'https://api.github.com/users/{username}/following')

    def follow_user(self, username):
        url = f'https://api.github.com/user/following/{username}'
        response = self._make_request('PUT', url)
        return response.status_code == 204

    def _get_paginated_data(self, url):
        page = 1
        data = []
        while True:
            paginated_url = f'{url}?page={page}'
            response = self._make_request('GET', paginated_url)

            if response.status_code != 200:
                raise Exception(f"Error fetching data from {paginated_url}. Status code: {response.status_code}")

            page_data = response.json()
            if not page_data:
                break  # No more data to fetch

            data.extend(page_data)
            page += 1

        return data

    def _make_request(self, method, url):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=self.headers)
                elif method == 'PUT':
                    response = requests.put(url, headers=self.headers)
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


class FollowBackFollowers:
    def __init__(self, client, username):
        self.client = client
        self.username = username

    def follow_back_periodically(self):
        while True:
            try:
                self.follow_back()
                time.sleep(120)  # Wait for 2 minutes before checking again
                logger.info("2 minutes after retry")
            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
                time.sleep(60)  # Wait for 1 minute before retrying
                logger.info("1 minute after retry")

    def follow_back(self):
        followers = self.client.get_followers(self.username)
        following = self.client.get_following(self.username)

        following_set = {user['login'] for user in following}

        for user in followers:
            if user['login'] not in following_set:
                success = self.client.follow_user(user['login'])
                if success:
                    logger.info(f"Successfully followed back {user['login']}")
                else:
                    logger.error(f"Failed to follow back {user['login']}")
