# Gmail Mail Client

A lightweight Python library for sending emails via Gmail using OAuth2 authentication. No more app passwords or plaintext credentials!

## Features

- 🔐 **Secure OAuth2 authentication** - No plaintext passwords
- 📧 **Simple API** - Send emails with just a few lines of code  
- 🖥️ **Command line interface** - Send emails from terminal
- 📦 **Lightweight** - Minimal dependencies
- 🔄 **Auto token refresh** - Handles expired tokens automatically
- 📨 **HTML & Plain text** - Support for both email formats
- 👥 **CC/BCC support** - Send to multiple recipients

## Installation

```bash
pip install .
```

## Quick Start

### 1. Setup OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API
4. Go to APIs & Services > Credentials
5. Click "Create Credentials" > "OAuth 2.0 Client IDs"
6. Choose "Desktop application"
7. Download the JSON file as `credentials.json`

### 2. Send Your First Email

```python
from mail import GmailClient, EmailMessage

# First run will open browser for authorization
client = GmailClient()

email = EmailMessage(
    to=["friend@example.com"],
    subject="Hello from Python!",
    body="This email was sent using the Gmail API with OAuth2!"
)

client.send_email(email)
print("Email sent successfully! ✓")
```

## Usage

### Python Library

```python
from mail import GmailClient, EmailMessage

# Initialize client (uses credentials.json and token.json by default)
client = GmailClient()

# Or specify custom file paths
client = GmailClient(
    credentials_file="path/to/credentials.json",
    token_file="path/to/token.json"
)

# Send plain text email
email = EmailMessage(
    to=["user@example.com"],
    subject="Meeting Reminder",
    body="Don't forget about our meeting at 3pm today!"
)
client.send_email(email)

# Send HTML email with CC/BCC
email = EmailMessage(
    to=["team@example.com"],
    cc=["manager@example.com"],
    bcc=["archive@example.com"],
    subject="Weekly Report",
    body="<h1>Weekly Report</h1><p>All tasks completed successfully!</p>",
    body_type="html"
)
client.send_email(email)

# Send email with custom from address
email = EmailMessage(
    to=["user@example.com"],
    subject="System Notification",
    body="Your backup has completed successfully."
)
client.send_email(email, from_addr="noreply@mycompany.com")
```

### Command Line Interface

```bash
# Simple email
gmail-send --to friend@example.com --subject "Hi" --body "Hello there!"

# HTML email with CC
gmail-send \
  --to user@example.com \
  --subject "Report" \
  --body "<h1>Monthly Report</h1><p>All systems operational.</p>" \
  --html \
  --cc boss@example.com

# Multiple recipients
gmail-send \
  --to user1@example.com user2@example.com \
  --subject "Team Update" \
  --body "Meeting moved to 4pm tomorrow"

# Custom from address
gmail-send \
  --to user@example.com \
  --from "notifications@mycompany.com" \
  --subject "System Alert" \
  --body "Server maintenance scheduled for tonight"

# Custom credential files
gmail-send \
  --to user@example.com \
  --subject "Test" \
  --body "Hello!" \
  --credentials /path/to/credentials.json \
  --token /path/to/token.json
```

### CLI Options

```
--to          Recipient email addresses (required)
--subject     Email subject (required)  
--body        Email body (required)
--from        Sender email address (optional, overrides default)
--cc          CC email addresses (optional)
--bcc         BCC email addresses (optional)
--html        Send as HTML email (optional)
--credentials Path to credentials.json file (optional)
--token       Path to token.json file (optional)
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Optional: Override default file paths
GMAIL_USERNAME=your-email@gmail.com
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
```

### File Structure

```
your-project/
├── credentials.json    # OAuth2 credentials from Google Cloud Console
├── token.json         # Auto-generated access tokens (created after first auth)
└── .env              # Optional environment variables
```

## Security

- **No plaintext passwords** - Uses OAuth2 tokens only
- **Automatic token refresh** - Handles expired access tokens
- **Local token storage** - Tokens stored securely on your machine
- **Minimal permissions** - Only requests Gmail send permission

## Troubleshooting

### First Time Setup

On first run, the library will:
1. Open your default browser
2. Ask you to sign in to Google
3. Request permission to send emails
4. Save tokens locally for future use

### Common Issues

**"Credentials file not found"**
- Make sure `credentials.json` is in your working directory
- Or specify the path: `GmailClient(credentials_file="path/to/credentials.json")`

**"Authentication Required"** 
- Delete `token.json` and re-authenticate
- Make sure Gmail API is enabled in Google Cloud Console

**"Permission denied"**
- Ensure the Google account has Gmail access
- Check that OAuth2 consent screen is configured

### Testing

```bash
# Run tests
pytest test_mail_client.py

# Install in development mode
pip install -e .
```

## API Reference

### EmailMessage

```python
EmailMessage(
    to: List[str],              # Required: recipient emails
    subject: str,               # Required: email subject
    body: str,                  # Required: email body
    body_type: str = "plain",   # Optional: "plain" or "html"
    cc: List[str] = None,       # Optional: CC recipients
    bcc: List[str] = None       # Optional: BCC recipients
)
```

### GmailClient

```python
GmailClient(
    credentials_file: str = "credentials.json",  # OAuth2 credentials
    token_file: str = "token.json"               # Stored access tokens
)

# Methods
client.send_email(email: EmailMessage, from_addr: str = None) -> bool
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Need help?** Create an issue on GitHub or check the troubleshooting section above.