import json
import time
from src.utils.logger import logger
import requests

class GitHubClientUnstar:
    def __init__(self, config, username):
        self.token = config.get_api_key()
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.username = username

    def get_starred_repos(self):
        return self._get_paginated_data(f'https://api.github.com/users/{self.username}/starred')

    def get_followers(self):
        return self._get_paginated_data(f'https://api.github.com/users/{self.username}/followers')

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
                elif method == 'DELETE':
                    response = requests.delete(url, headers=self.headers)
                else:
                    raise ValueError("Unsupported HTTP method")
                return response
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                time.sleep(2 ** attempt)
        raise Exception(f"Failed to {method} {url} after {max_retries} attempts")

    def unstar_repo(self, owner, repo):
        url = f'https://api.github.com/user/starred/{owner}/{repo}'
        response = self._make_request('DELETE', url)
        if response.status_code == 204:
            logger.info(f"Successfully unstarred {owner}/{repo}")
        else:
            logger.error(f"Failed to unstar {owner}/{repo}. Status code: {response.status_code}")

    def unstar_non_followers_repos(self):
        followers = {follower['login'] for follower in self.get_followers()}
        starred_repos = self.get_starred_repos()

        for repo in starred_repos:
            owner = repo['owner']['login']
            if owner == "Errahum":
                logger.info(f"Skipping {owner}'s repo as it should never be unstarred")
                continue
            if owner not in followers:
                self.unstar_repo(owner, repo['name'])
