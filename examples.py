#!/usr/bin/env python3
"""
Gmail Mail Client - Usage Examples

This file demonstrates various ways to use the Gmail Mail Client library.
Make sure you have set up OAuth2 credentials first (see setup_oauth.md).
"""

from mail import GmailClient, EmailMessage


def example_basic_email():
    """Send a basic plain text email"""
    print("📧 Sending basic email...")
    
    client = GmailClient()
    
    email = EmailMessage(
        to=["friend@example.com"],
        subject="Hello from Python!",
        body="This is a simple plain text email sent using the Gmail API."
    )
    
    success = client.send_email(email)
    if success:
        print("✅ Basic email sent successfully!")
    else:
        print("❌ Failed to send basic email")


def example_html_email():
    """Send an HTML formatted email"""
    print("🎨 Sending HTML email...")
    
    client = GmailClient()
    
    html_body = """
    <html>
        <body>
            <h1 style="color: #4285f4;">Weekly Report</h1>
            <p>Dear Team,</p>
            <ul>
                <li>✅ Project Alpha completed</li>
                <li>🔄 Project Beta in progress</li>
                <li>📅 Project Gamma scheduled for next week</li>
            </ul>
            <p>Best regards,<br>
            <strong>Your Automated System</strong></p>
        </body>
    </html>
    """
    
    email = EmailMessage(
        to=["team@example.com"],
        subject="📊 Weekly Status Report",
        body=html_body,
        body_type="html"
    )
    
    success = client.send_email(email)
    if success:
        print("✅ HTML email sent successfully!")
    else:
        print("❌ Failed to send HTML email")


def example_multiple_recipients():
    """Send email to multiple recipients with CC and BCC"""
    print("👥 Sending email to multiple recipients...")
    
    client = GmailClient()
    
    email = EmailMessage(
        to=["user1@example.com", "user2@example.com"],
        cc=["manager@example.com"],
        bcc=["archive@example.com"],
        subject="Team Meeting Tomorrow",
        body="Hi everyone,\n\nReminder: We have a team meeting tomorrow at 2 PM in Conference Room A.\n\nThanks!"
    )
    
    success = client.send_email(email)
    if success:
        print("✅ Multi-recipient email sent successfully!")
    else:
        print("❌ Failed to send multi-recipient email")


def example_notification_email():
    """Send a system notification email"""
    print("🔔 Sending notification email...")
    
    client = GmailClient()
    
    email = EmailMessage(
        to=["admin@example.com"],
        subject="🚨 System Alert: High CPU Usage",
        body="Alert: Server CPU usage has exceeded 90% for the past 5 minutes.\n\nServer: prod-web-01\nCurrent CPU: 94%\nTime: 2024-03-15 14:30:00 UTC\n\nPlease investigate immediately."
    )
    
    success = client.send_email(email)
    if success:
        print("✅ Notification email sent successfully!")
    else:
        print("❌ Failed to send notification email")


def example_custom_credentials():
    """Use custom credential file paths"""
    print("🔧 Using custom credential paths...")
    
    # You can specify custom paths for credentials and token files
    client = GmailClient(
        credentials_file="custom_credentials.json",
        token_file="custom_token.json"
    )
    
    email = EmailMessage(
        to=["test@example.com"],
        subject="Custom Credentials Test",
        body="This email was sent using custom credential file paths."
    )
    
    try:
        success = client.send_email(email)
        if success:
            print("✅ Email with custom credentials sent successfully!")
        else:
            print("❌ Failed to send email with custom credentials")
    except Exception as e:
        print(f"❌ Error with custom credentials: {e}")


def example_error_handling():
    """Demonstrate proper error handling"""
    print("⚠️  Demonstrating error handling...")
    
    try:
        client = GmailClient()
        
        email = EmailMessage(
            to=["invalid-email"],  # This will cause a validation error
            subject="Test",
            body="This should fail validation"
        )
        
        success = client.send_email(email)
        
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
    except RuntimeError as e:
        print(f"❌ Runtime Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


def main():
    """Run all examples"""
    print("🚀 Gmail Mail Client - Examples\n")
    
    examples = [
        example_basic_email,
        example_html_email,
        example_multiple_recipients,
        example_notification_email,
        example_custom_credentials,
        example_error_handling
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n--- Example {i}: {example.__doc__} ---")
        try:
            example()
        except Exception as e:
            print(f"❌ Example failed: {e}")
        print()
    
    print("🏁 All examples completed!")


if __name__ == "__main__":
    main()