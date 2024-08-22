import json
import time
import requests
from src.utils.logger import logger

class GitHubClientFollow:
    def __init__(self, config):
        self.token = config.get_api_key()
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.authenticated_user = self.get_authenticated_user()

    def get_authenticated_user(self):
        user_url = 'https://api.github.com/user'
        response = self._make_request_follow('GET', user_url)
        if response.status_code != 200:
            raise Exception(f"Error fetching authenticated user. Status code: {response.status_code}")
        return response.json()['login']

    def get_followers(self, username):
        return self._get_paginated_data(f'https://api.github.com/users/{username}/followers')

    def get_following(self, username):
        return self._get_paginated_data(f'https://api.github.com/users/{username}/following')

    def get_user(self, username):
        user_url = f'https://api.github.com/users/{username}'
        response = self._make_request_follow('GET', user_url)
        if response.status_code != 200:
            raise Exception(f"Error fetching user {username}. Status code: {response.status_code}")
        return response.json()

    def star_project(self, owner, repo):
        star_url = f'https://api.github.com/user/starred/{owner}/{repo}'
        response = self._make_request_follow('PUT', star_url)
        if response.status_code == 204:
            logger.info(f"Successfully starred the project {repo} by {owner}.")
        else:
            logger.error(f"Failed to star the project {repo} by {owner}. Status code: {response.status_code}")

    def _get_paginated_data(self, url):
        page = 1
        data = []
        while True:
            paginated_url = f'{url}?page={page}'
            response = self._make_request_follow('GET', paginated_url)

            if response.status_code != 200:
                raise Exception(f"Error fetching data from {paginated_url}. Status code: {response.status_code}")

            page_data = response.json()
            if not page_data:
                break

            data.extend(page_data)
            page += 1

        return data

    def _make_request_follow(self, method, url):
        max_retries = 3
        retry_delay = 10

        for attempt in range(max_retries):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=self.headers)
                elif method == 'PUT':
                    response = requests.put(url, headers=self.headers)
                else:
                    raise ValueError("Unsupported HTTP method")

                if response.status_code == 429:
                    logger.error(f"Server error (429) at {url}, retrying... {retry_delay} seconds.")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue

                if response.status_code == 500:
                    logger.error(f"Server error (500) at {url}, retrying...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue

                return response

            except requests.RequestException as e:
                logger.error(f"Request to {url} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    logger.error(f"All retries exhausted for {url}. Returning None.")
                    return None

        return None


class FollowerManager:
    def __init__(self, client, max_peoples_follow, jsonl_file):
        self.client = client
        self.max_peoples_follow = max_peoples_follow
        self.jsonl_file = jsonl_file
        self.ensure_following_errahum()

    def select_valid_users(self, followers, following, condition_follow=False):
        valid_users = []
        follower_set = {user['login'] for user in followers}
        following_set = {user['login'] for user in following}

        common_users = follower_set.intersection(following_set)

        logger.info(f"Common users: {common_users}")
        logger.info(f"Using condition_follow? {condition_follow}")

        for user in common_users:
            if user == self.client.authenticated_user:
                logger.info(f"Skipping self: {user}")
                continue

            user_data = self.client.get_user(user)
            num_following = user_data['following']

            if self.is_in_jsonl(user):
                logger.info(f"{user} is already in JSONL file, skipping follow.")
                continue

            check_response = self.is_following(user)

            if check_response.status_code == 204:
                logger.info(f"Already following {user}")
                continue  # Skip to the next user

            logger.info(f"Checking user: {user}, following count: {num_following}")

            if condition_follow:
                if 2 < num_following < 10 or num_following > 10000:
                    valid_users.append(user_data)
                    logger.info(f"Added user {user} to valid users.")
            else:
                valid_users.append(user_data)
                logger.info(f"Added user {user} to valid users.")

            if len(valid_users) >= self.max_peoples_follow:
                break

        return valid_users

    def is_following(self, username):
        # Check if already following the user
        check_following_url = f'https://api.github.com/user/following/{username}'
        check_response = requests.get(check_following_url, headers=self.client.headers)

        return check_response

    def is_in_jsonl(self, username):
        # Check if username is already in JSONL file
        with open(self.jsonl_file, 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                if data == username:
                    return True
        return False

    def follow_users(self, users):
        for user in users:
            follow_url = f'https://api.github.com/user/following/{user["login"]}'

            # Follow the user
            response = self.client._make_request_follow('PUT', follow_url)

            if response.status_code == 204:
                logger.info(f"Successfully followed {user['login']}")
                self.star_pinned_projects([user["login"]])
            else:
                logger.error(f"Failed to follow {user['login']} with status code {response.status_code}")

    def star_pinned_projects(self, usernames):
        query = """
        query($username: String!) {
            user(login: $username) {
                pinnedItems(first: 1, types: REPOSITORY) {
                    nodes {
                        ... on Repository {
                            name
                            owner {
                                login
                            }
                        }
                    }
                }
            }
        }
        """
        headers = {
            'Authorization': f'token {self.client.token}',
            'Content-Type': 'application/json'
        }

        for username in usernames:
            variables = {"username": username}
            response = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch pinned projects for {username}. Status code: {response.status_code}")
                continue

            data = response.json()
            pinned_projects = data['data']['user']['pinnedItems']['nodes']
            
            if pinned_projects:
                first_project = pinned_projects[0]
                self.client.star_project(first_project['owner']['login'], first_project['name'])
            else:
                logger.info(f"No pinned projects found for {username}.")

    def ensure_following_errahum(self):
        errahum_username = "Errahum"
        check_response = self.is_following(errahum_username)
        if check_response.status_code != 204:

            follow_url = f'https://api.github.com/user/following/{errahum_username}'
            response = self.client._make_request_follow('PUT', follow_url)
            if response.status_code == 204:
                logger.info(f"Successfully followed {errahum_username}")
            else:
                logger.error(f"Failed to follow {errahum_username} with status code {response.status_code}")


        self.star_pinned_projects([errahum_username])

def extract_username_from_url(url):
    parts = url.split('/')
    if len(parts) > 3 and parts[2] == "github.com":
        return parts[3]
    else:
        raise ValueError("Invalid GitHub profile URL")