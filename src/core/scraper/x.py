import json
import time
import requests
from src.utils.logger import logger

class XScraper:
    def __init__(self, config, max_accounts):
        self.github_token = config.get_api_key()
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.jsonl_file = "X_profiles.jsonl"
        self.max_accounts = max_accounts

    def get_github_followers(self, username, max_accounts):
        url = f'https://api.github.com/users/{username}/followers'
        self.max_accounts = max_accounts
        followers = self._get_paginated_data(url)
        X_profiles = self._extract_X_profiles(followers)
        self._update_jsonl_file(X_profiles)

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
                break

            data.extend(page_data)
            if len(data) >= self.max_accounts:
                data = data[:self.max_accounts]
                break

            page += 1

        return data

    def _update_jsonl_file(self, X_profiles):
        valid_profiles = [profile for profile in X_profiles if self._is_valid_X(profile['X_url'])]
        with open(self.jsonl_file, 'w') as file:
            for profile in valid_profiles:
                file.write(json.dumps(profile) + '\n')

    def _is_valid_X(self, X_url):
        # Placeholder for actual X URL validation logic
        return True

    def _make_request(self, method, url):
        for _ in range(3):
            try:
                response = requests.request(method, url, headers=self.headers)
                if response.status_code in [500, 429]:
                    time.sleep(10)
                    continue
                return response
            except requests.RequestException as e:
                logger.error(f"Request to {url} failed: {e}")
                time.sleep(10)
        return None

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
                break

            data.extend(page_data)
            if len(data) >= self.max_accounts:
                data = data[:self.max_accounts]
                break

            page += 1

        return data

    def _extract_X_profiles(self, followers):
        X_profiles = []
        for follower in followers:
            social_accounts_url = f"https://api.github.com/users/{follower['login']}/social_accounts"
            response = self._make_request('GET', social_accounts_url)
            if response.status_code == 200:
                social_accounts = response.json()
                X_url = next((account['url'] for account in social_accounts if 'x.com' in account['url']), None)
                if X_url:
                    X_profiles.append({'github_username': follower['login'], 'X_url': X_url})
        return X_profiles

    def _update_jsonl_file(self, X_profiles):
        valid_profiles = [profile for profile in X_profiles if self._is_valid_X(profile['X_url'])]
        with open(self.jsonl_file, 'w') as file:
            for profile in valid_profiles:
                file.write(json.dumps(profile) + '\n')

    def _is_valid_X(self, X_url):
        # Placeholder for actual X URL validation logic
        return True

    def _make_request(self, method, url):
        for _ in range(3):
            try:
                response = requests.request(method, url, headers=self.headers)
                if response.status_code in [500, 429]:
                    time.sleep(10)
                    continue
                return response
            except requests.RequestException as e:
                logger.error(f"Request to {url} failed: {e}")
                time.sleep(10)
        return None

    def scrape_X_profiles(self, followers):
        if followers is None:
            logger.error("Followers list is None, cannot scrape X profiles.")
            return

        X_profiles = []
        existing_profiles = self.load_existing_profiles()

        for follower in followers:
            username = follower['login']
            X_url = f"https://x.com/{username}"

            if X_url in existing_profiles:
                logger.info(f"X profile for {username} already exists, skipping.")
                continue

            X_profiles.append({
                "github_username": username,
                "X_url": X_url
            })

            if len(X_profiles) >= self.max_accounts:
                break

        self.save_profiles_to_jsonl(X_profiles)

    def load_existing_profiles(self):
        existing_profiles = set()
        try:
            with open(self.jsonl_file, 'r') as file:
                for line in file:
                    data = json.loads(line.strip())
                    existing_profiles.add(data['X_url'])
        except FileNotFoundError:
            pass
        return existing_profiles

    def save_profiles_to_jsonl(self, profiles):
        with open(self.jsonl_file, 'a') as file:
            for profile in profiles:
                json.dump(profile, file)
                file.write('\n')
        logger.info(f"Saved {len(profiles)} new X profiles to {self.jsonl_file}.")
