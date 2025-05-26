import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from src.mail.mail_client import EmailMessage, GmailClient


class TestEmailMessage:
    """Test EmailMessage model"""
    
    def test_basic_email_message(self):
        email = EmailMessage(
            to=["test@example.com"],
            subject="Test Subject",
            body="Test body"
        )
        assert email.to == ["test@example.com"]
        assert email.subject == "Test Subject"
        assert email.body == "Test body"
        assert email.body_type == "plain"
    
    def test_html_email_message(self):
        email = EmailMessage(
            to=["test@example.com"],
            subject="Test Subject",
            body="<h1>Test HTML</h1>",
            body_type="html"
        )
        assert email.body_type == "html"
    
    def test_email_with_cc_bcc(self):
        email = EmailMessage(
            to=["test@example.com"],
            subject="Test Subject",
            body="Test body",
            cc=["cc@example.com"],
            bcc=["bcc@example.com"]
        )
        assert email.cc == ["cc@example.com"]
        assert email.bcc == ["bcc@example.com"]


class TestGmailClient:
    """Test GmailClient with OAuth2"""
    
    @patch('src.mail.mail_client.Path.exists')
    @patch('src.mail.mail_client.Credentials.from_authorized_user_file')
    @patch.dict(os.environ, {"GMAIL_USERNAME": "test@gmail.com"})
    def test_client_initialization_with_token(self, mock_creds_from_file, mock_exists):
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds_from_file.return_value = mock_creds
        
        client = GmailClient()
        assert client.username == "test@gmail.com"
        assert client.credentials == mock_creds
    
    @patch('src.mail.mail_client.Path.exists')
    def test_client_missing_credentials_file(self, mock_exists):
        mock_exists.return_value = False
        
        with pytest.raises(ValueError, match="Credentials file not found"):
            GmailClient()
    
    @patch('src.mail.mail_client.Path.exists')
    @patch('src.mail.mail_client.Credentials.from_authorized_user_file')
    @patch('src.mail.mail_client.build')
    @patch.dict(os.environ, {"GMAIL_USERNAME": "test@gmail.com"})
    def test_send_email_success(self, mock_build, mock_creds_from_file, mock_exists):
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds.expired = False
        mock_creds_from_file.return_value = mock_creds
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.users().messages().send().execute.return_value = {'id': 'message123'}
        
        client = GmailClient()
        email = EmailMessage(
            to=["recipient@example.com"],
            subject="Test",
            body="Test body"
        )
        
        result = client.send_email(email)
        assert result is True
        mock_service.users().messages().send.assert_called_once()
    
    @patch('src.mail.mail_client.Path.exists')
    @patch('src.mail.mail_client.Credentials.from_authorized_user_file')
    @patch('src.mail.mail_client.build')
    @patch.dict(os.environ, {"GMAIL_USERNAME": "test@gmail.com"})
    def test_send_email_with_custom_from(self, mock_build, mock_creds_from_file, mock_exists):
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds.expired = False
        mock_creds_from_file.return_value = mock_creds
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.users().messages().send().execute.return_value = {'id': 'message123'}
        
        client = GmailClient()
        email = EmailMessage(
            to=["recipient@example.com"],
            subject="Test",
            body="Test body"
        )
        
        result = client.send_email(email, from_addr="custom@example.com")
        assert result is True
        mock_service.users().messages().send.assert_called_once()
    
    @patch('src.mail.mail_client.Path.exists')
    @patch('src.mail.mail_client.Credentials.from_authorized_user_file')
    @patch('src.mail.mail_client.build')
    @patch.dict(os.environ, {"GMAIL_USERNAME": "test@gmail.com"})
    def test_send_email_failure(self, mock_build, mock_creds_from_file, mock_exists):
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds.expired = False
        mock_creds_from_file.return_value = mock_creds
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.users().messages().send().execute.side_effect = Exception("API Error")
        
        client = GmailClient()
        email = EmailMessage(
            to=["recipient@example.com"],
            subject="Test",
            body="Test body"
        )
        
        with pytest.raises(RuntimeError, match="Failed to send email: API Error"):
            client.send_email(email)