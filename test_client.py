from mail import GmailClient, EmailMessage

client = GmailClient()  # Uses OAuth2, no passwords needed
email = EmailMessage(to=["repque@yahoo.com"], subject="Hello", body="Test")
client.send_email(email)


