# How to Create Your GitHub Personal Access Token

GitHub offers a way to authenticate to their API using Personal Access Tokens. Follow these steps to create your GitHub Personal Access Token:

1. **Create a GitHub Account:**
   - Go to the GitHub website (https://github.com/).
   - Click on "Sign Up" to create an account if you don't already have one.

2. **Access Your Account:**
   - Once logged in, navigate to your GitHub account settings.

3. **Go to the Developer Settings:**
   - In your GitHub account, click on your profile picture in the upper right corner.
   - Select "Settings" from the dropdown menu.
   - Scroll down to the "Developer settings" section on the left sidebar and click on it.

4. **Generate a New Token:**
   - Click on "Personal access tokens" under the "Developer settings".
   - Click the "Generate new token" button.
   - Give your token a descriptive name and select the scopes or permissions you need.

5. **Copy Your Token:**
   - Once the token is generated, copy it. It will look something like `ghp_XXXXXXXXXXXXXXXXXXXXXX`.

6. **Keep Your Token Secure:**
   - It's important to keep your token secure and not share it publicly.

7. **Use Your Token:**
   - You can now use your token to access GitHub services from your application.

8. **Manage Your Token:**
   - In your GitHub account, you can manage your tokens, create new ones, or revoke them if necessary.

That's it! You have now created your GitHub Personal Access Token and are ready to start using the GitHub API for your projects.

# Setting Up an Environment Variable for the GitHub Personal Access Token on Windows

To use the GitHub API in your Windows environment, you need to set up an environment variable to store your token. Here's how:

1. **Find Advanced System Settings:**
   - Right-click on "This PC" or "Computer" in File Explorer or on the desktop.
   - Select "Properties" from the context menu.
   - Click on "Advanced system settings" on the left side of the window.

2. **Open Environment Variables:**
   - In the "System Properties" window, click the "Environment Variables..." button near the bottom of the window.

3. **Add a New Environment Variable:**
   - In the "System Variables" or "User Variables" section, click "New...".
   - For "Variable name", enter: `GITHUB_FOLLOW_UNFOLLOW`.
   - For "Variable value", enter your GitHub Personal Access Token.

4. **Confirm and Apply Changes:**
   - Click "OK" to close the "New System Variable" or "New User Variable" window.
   - Click "OK" to close the "Environment Variables" window.
   - Click "OK" to close the "System Properties" window.

5. **Restart Your Computer:**
   - To apply the changes, you may need to restart your computer.

Your `GITHUB_FOLLOW_UNFOLLOW` environment variable is now set up for use in your Windows environment.
