import requests


class GitHubClientGetFollowings:
    def __init__(self, config):
        self.token = config.get_api_key()
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_following(self, username):
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
                print(f"Server error (500) at {url}, retrying...")
                # Handle retries if needed

            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Request to {url} failed: {e}")
            raise
