import base64
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydantic import BaseModel, EmailStr, Field


class EmailMessage(BaseModel):
    """Email message model"""
    to: List[EmailStr]
    subject: str
    body: str
    body_type: str = Field(default="plain", description="'plain' or 'html'")
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None


class GmailClient:
    """Simple Gmail API client with OAuth2 authentication"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    def __init__(self, credentials_file: Optional[str] = None, token_file: Optional[str] = None):
        # Default file paths
        self.credentials_file = credentials_file or os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
        self.token_file = token_file or os.getenv("GMAIL_TOKEN_FILE", "token.json")
        
        self.credentials = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.credentials)
        self.username = self._extract_email_from_token()
    
    def _get_credentials(self) -> Credentials:
        """Get OAuth2 credentials, refreshing or creating as needed"""
        creds = None
        
        # Load existing token
        if Path(self.token_file).exists():
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not Path(self.credentials_file).exists():
                    raise ValueError(f"Credentials file not found: {self.credentials_file}")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next time
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def _extract_email_from_token(self) -> str:
        """Extract email from token file"""
        if Path(self.token_file).exists():
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
                # Google tokens don't always include email, use a default or require env var
                return token_data.get('client_id', '').split('@')[0] + '@gmail.com'
        
        # Fallback to env var
        email = os.getenv("GMAIL_USERNAME")
        if not email:
            raise ValueError("Cannot determine email address. Set GMAIL_USERNAME env var.")
        return email
    
    def send_email(self, email: EmailMessage) -> bool:
        """Send an email via Gmail API"""
        try:
            # Create MIME message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(email.to)
            msg['Subject'] = email.subject
            
            if email.cc:
                msg['Cc'] = ', '.join(email.cc)
            if email.bcc:
                msg['Bcc'] = ', '.join(email.bcc)
            
            msg.attach(MIMEText(email.body, email.body_type))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
            
            # Send via Gmail API
            message = {'raw': raw_message}
            result = self.service.users().messages().send(userId='me', body=message).execute()
            
            return bool(result.get('id'))
            
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}")