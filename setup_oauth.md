# Gmail OAuth2 Setup Guide

## Overview

This guide walks you through setting up OAuth2 authentication for the Gmail Mail Client. OAuth2 is more secure than app passwords and provides granular permissions.

## Step 1: Google Cloud Console Setup

### 1.1 Create or Select Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project name/ID for reference

### 1.2 Enable Gmail API
1. In the Google Cloud Console, go to **APIs & Services > Library**
2. Search for "Gmail API"
3. Click on "Gmail API" and click **Enable**
4. Wait for the API to be enabled (may take a few minutes)

### 1.3 Configure OAuth Consent Screen
1. Go to **APIs & Services > OAuth consent screen**
2. Choose **External** user type (unless you have Google Workspace)
3. Fill in required fields:
   - App name: "Gmail Mail Client" (or your app name)
   - User support email: Your email
   - Developer contact: Your email
4. Click **Save and Continue**
5. Skip Scopes section (click **Save and Continue**)
6. Add test users (your Gmail address) if in testing mode
7. Click **Save and Continue**

## Step 2: Create OAuth2 Credentials

### 2.1 Create Desktop Application Credentials
1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth 2.0 Client IDs**
3. Choose **Desktop application** as application type
4. Enter name: "Gmail Mail Client Desktop"
5. Click **Create**

### 2.2 Download Credentials
1. Click the download icon next to your newly created OAuth client
2. Save the JSON file as `credentials.json` in your project directory
3. **Keep this file secure** - it contains your OAuth2 client secrets

## Step 3: First Run Authentication

### 3.1 Install and Run
```bash
pip install .
```

```python
from mail import GmailClient, EmailMessage

# This will open browser for first-time authorization
client = GmailClient()
email = EmailMessage(
    to=["test@example.com"], 
    subject="OAuth2 Test", 
    body="This email confirms OAuth2 is working!"
)
client.send_email(email)
```

### 3.2 Authorization Flow
1. Browser opens automatically
2. Sign in to your Google account
3. Review permissions (Gmail send access)
4. Click "Allow"
5. You may see "This app isn't verified" - click "Advanced > Go to [App Name] (unsafe)"
6. Grant permission to send emails
7. Browser shows "The authentication flow has completed"

## Step 4: Subsequent Usage

After first authorization:
- `token.json` file is created automatically
- No browser interaction needed for future runs
- Tokens refresh automatically when expired

## File Structure

```
your-project/
├── credentials.json    # OAuth2 client credentials (from Step 2)
├── token.json         # Access/refresh tokens (auto-created in Step 3)
├── .env              # Optional: environment variable overrides
└── your-script.py    # Your Python code
```

## Security Best Practices

### Credential Files
- **Never commit `credentials.json` to version control**
- **Never commit `token.json` to version control**
- Add both to `.gitignore`
- Store credentials securely in production

### Production Deployment
For production environments:
```bash
# Set environment variables instead of files
export GMAIL_CREDENTIALS_FILE=/secure/path/credentials.json
export GMAIL_TOKEN_FILE=/secure/path/token.json
export GMAIL_USERNAME=your-app@example.com
```

## Troubleshooting

### "This app isn't verified"
- This is normal for personal projects
- Click "Advanced > Go to [App Name] (unsafe)"
- For production apps, submit for Google verification

### "Access blocked: This app's request is invalid"
- Ensure OAuth consent screen is configured
- Check that Gmail API is enabled
- Verify redirect URI matches (should be localhost for desktop apps)

### "Credentials file not found"
- Ensure `credentials.json` is in the correct location
- Check file permissions (readable by your script)
- Verify file path in code or environment variables

### "Permission denied"
- Delete `token.json` and re-authenticate
- Ensure the Google account has Gmail access
- Check that scopes include 'https://www.googleapis.com/auth/gmail.send'

### "Token refresh failed"
- Delete `token.json` and re-authenticate
- Check internet connectivity
- Ensure credentials haven't been revoked in Google Account settings

## Advanced Configuration

### Custom Scopes
```python
# Default scope is gmail.send only
# For reading emails, modify SCOPES in mail_client.py:
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]
```

### Environment Variables
```bash
# .env file
GMAIL_USERNAME=your-email@gmail.com
GMAIL_CREDENTIALS_FILE=/path/to/credentials.json
GMAIL_TOKEN_FILE=/path/to/token.json
```

### Multiple Accounts
```python
# Use different token files for different accounts
client1 = GmailClient(
    credentials_file="account1_credentials.json",
    token_file="account1_token.json"
)

client2 = GmailClient(
    credentials_file="account2_credentials.json", 
    token_file="account2_token.json"
)
```

## Getting Help

- Check the main [README.md](README.md) for usage examples
- Review [Google's OAuth2 documentation](https://developers.google.com/identity/protocols/oauth2)
- Create an issue on GitHub for specific problems

---

**Next Steps:** Once OAuth2 is set up, see the main README.md for usage examples and API documentation.