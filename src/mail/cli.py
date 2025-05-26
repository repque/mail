#!/usr/bin/env python3
"""Command line interface for Gmail client"""

import argparse
import sys
from typing import List

from mail_client import EmailMessage, GmailClient


def main():
    parser = argparse.ArgumentParser(description="Send emails via Gmail using OAuth2")
    parser.add_argument("--to", required=True, nargs="+", help="Recipient email addresses")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body")
    parser.add_argument("--from", dest="from_addr", help="Sender email address (overrides default)")
    parser.add_argument("--cc", nargs="*", help="CC email addresses")
    parser.add_argument("--bcc", nargs="*", help="BCC email addresses")
    parser.add_argument("--html", action="store_true", help="Send as HTML email")
    parser.add_argument("--credentials", help="Path to credentials.json file")
    parser.add_argument("--token", help="Path to token.json file")
    
    args = parser.parse_args()
    
    try:
        # Create client
        client = GmailClient(
            credentials_file=args.credentials,
            token_file=args.token
        )
        
        # Create email
        email = EmailMessage(
            to=args.to,
            subject=args.subject,
            body=args.body,
            body_type="html" if args.html else "plain",
            cc=args.cc,
            bcc=args.bcc
        )
        
        # Send email
        success = client.send_email(email, from_addr=args.from_addr)
        
        if success:
            print(f"✓ Email sent successfully to {', '.join(args.to)}")
            return 0
        else:
            print("✗ Failed to send email")
            return 1
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())