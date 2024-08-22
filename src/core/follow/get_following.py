import requests
from src.utils.logger import logger

class GitHubClientGetFollowings:
    def __init__(self, config):
        self.token = config.get_api_key()
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.auth_user = self._get_authenticated_user()

    def _get_authenticated_user(self):
        try:
            response = self._make_request('GET', 'https://api.github.com/user')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch authenticated user: {e}")
            raise

    def get_following(self):
        if not self.auth_user:
            raise ValueError("Authenticated user information not available")

        username = self.auth_user.get('login')
        if not username:
            raise ValueError("Username not found in authenticated user data")

        return self._get_paginated_data(f'https://api.github.com/users/{username}/following')

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
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            else:
                raise ValueError("Unsupported HTTP method")

            if response.status_code == 500:
                logger.error(f"Server error (500) at {url}, retrying...")
                # Handle retries if needed

            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Request to {url} failed: {e}")
            raise
