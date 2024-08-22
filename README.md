# GitFollowBot

GitFollowBot is an automation tool designed to manage your GitHub following and followers efficiently. With GitFollowBot, you can automatically follow users based on specific criteria and unfollow users who do not follow you back. This project aims to simplify the process of growing and managing your GitHub network.
Added support for gtihub accounts linked to Linkedin.

### Video
[![Alt text](https://i.imgur.com/4qOsG3m.gif)](https://www.youtube.com/watch?v=yXn_ygUheTE)

### **Disclaimer**
The use of GitFollowBot to automate GitHub actions such as following and unfollowing users should comply with [GitHub's terms of service](https://docs.github.com/en/github/site-policy/github-terms-of-service). Automated actions may affect your GitHub account's standing if used excessively or in violation of [GitHub's guidelines](https://docs.github.com/en/github/site-policy/github-acceptable-use-policies). Use GitFollowBot responsibly.
For Linkedin, X, you need to use my tools carefully to avoid having your account blocked.

**Important:** By using GitFollowBot, you agree to adhere to the terms of service of both GitHub and LinkedIn. Misuse of this tool can lead to your account being suspended or banned. Always ensure that your actions are within the acceptable use policies of these platforms.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Resources](#resources)
- [Contribute](#contribute)
- [License](#license)
- [Donate](#donate)

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have a GitHub account.
- You have Python 3.6 or higher installed on your computer.
- You have a GitHub personal access token with appropriate permissions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/GitFollowBot.git
    ```
2. Navigate to the project directory:
    ```bash
    cd GitFollowBot
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Configure your settings in the `config.py` file with your GitHub personal access token.
2. Run the main script:
    ```bash
    python main.py
    ```
3. Follow the on-screen instructions to choose an action (follow or unfollow users).

### Example Code Snippet

```python
from config import Config
from follow_unfollow.src.manager_follow_unfollow import MainFollowUnfollow

def main_console_follow_unfollow():
    config = Config()
    main_app = MainFollowUnfollow(config)
    while True:
        print("\nChoose an action:")
        print("1. Follow people")
        print("2. Unfollow people")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            main_app.follow_people()
        elif choice == '2':
            main_app.unfollow_people()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_console_follow_unfollow()
```

## Resources

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Python Requests Library](https://docs.python-requests.org/en/latest/)

## Contribute

Please contact me before contributing.
Contributions are always welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Donate

If you find this project helpful, consider supporting us with a donation to help maintain and improve the project. Thank you!

[![learning_application](https://i.imgur.com/abEFO5o.png)](https://buymeacoffee.com/Errahum)
