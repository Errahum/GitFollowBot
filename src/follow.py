import time
import requests


class GitHubClientFollow:
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

    def get_user(self, username):
        user_url = f'https://api.github.com/users/{username}'
        response = self._make_request_follow('GET', user_url)
        if response.status_code != 200:
            raise Exception(f"Error fetching user {username}. Status code: {response.status_code}")
        return response.json()

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
                break  # No more data to fetch

            data.extend(page_data)
            page += 1

        return data

    def _make_request_follow(self, method, url):
        max_retries = 1
        retry_delay = 2  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=self.headers)
                elif method == 'PUT':
                    response = requests.put(url, headers=self.headers)
                else:
                    raise ValueError("Unsupported HTTP method")

                if response.status_code == 500:
                    print(f"Server error (500) at {url}, retrying...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue  # Retry the request

                return response

            except requests.RequestException as e:
                print(f"Request to {url} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue  # Retry the request
                else:
                    raise


class FollowerManager:
    def __init__(self, client, max_peoples_follow):
        self.client = client
        self.max_peoples_follow = max_peoples_follow

    def select_valid_users(self, followers, following, condition_follow=True):
        valid_users = []
        follower_set = {user['login'] for user in followers}
        following_set = {user['login'] for user in following}

        common_users = follower_set.intersection(following_set)

        print(f"Common users: {common_users}")

        for user in common_users:
            user_data = self.client.get_user(user)
            num_following = user_data['following']

            print(f"Checking user: {user}, following count: {num_following}")

            if condition_follow:
                if 2 < num_following < 10 or num_following > 10000:
                    valid_users.append(user_data)
                    print(f"Added user {user} to valid users.")
            else:
                valid_users.append(user_data)
                print(f"Added user {user} to valid users.")

            if len(valid_users) >= self.max_peoples_follow:
                break

        return valid_users

    def follow_users(self, users):
        for user in users:
            follow_url = f'https://api.github.com/user/following/{user["login"]}'

            # Check if already following the user
            check_following_url = f'https://api.github.com/user/following/{user["login"]}'
            check_response = requests.get(check_following_url, headers=self.client.headers)

            if check_response.status_code == 204:
                print(f"Already following {user['login']}")
                continue  # Skip to the next user

            # Follow the user
            response = self.client._make_request_follow('PUT', follow_url)

            if response.status_code == 204:
                print(f"Successfully followed {user['login']}")
            else:
                print(f"Failed to follow {user['login']} with status code {response.status_code}")


def extract_username_from_url(url):
    parts = url.split('/')
    if len(parts) > 3 and parts[2] == "github.com":
        return parts[3]
    else:
        raise ValueError("Invalid GitHub profile URL")
