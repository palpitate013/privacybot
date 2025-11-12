# Proton Mail Bridge Configuration Guide

This guide explains how to configure PrivacyBot to work with Proton Mail Bridge.

## What is Proton Mail Bridge?

Proton Mail Bridge is a desktop application that allows you to use ProtonMail with standard email clients and applications via SMTP and IMAP protocols. It runs locally on your computer and acts as a secure bridge between your email applications and ProtonMail's servers.

## Prerequisites

1. A ProtonMail account (free or paid)
2. Proton Mail Bridge installed on your computer
   - Download from: https://protonmail.com/bridge
   - Available for Windows, macOS, and Linux

## Step-by-Step Setup

### 1. Install and Configure Proton Mail Bridge

1. Download Proton Mail Bridge from https://protonmail.com/bridge
2. Install the application for your operating system
3. Launch Proton Mail Bridge
4. Sign in with your ProtonMail account credentials
5. In Bridge, go to Settings and note the following:
   - SMTP Server: Usually `127.0.0.1` or `localhost`
   - SMTP Port: Usually `1025`
   - Your Bridge username (typically your email address)
   - Your Bridge password (NOT your ProtonMail password - Bridge generates this)

**Important**: The Bridge password is different from your ProtonMail password. You can view or regenerate it in the Bridge application settings.

### 2. Configure PrivacyBot

You have two options for configuration:

#### Option A: Using a Configuration File (Recommended)

1. Navigate to the `app` directory
2. Copy the example configuration:
   ```bash
   cp email_config.example.json email_config.json
   ```

3. Edit `email_config.json` with your Bridge credentials:
   ```json
   {
       "email_provider": "smtp",
       "smtp_settings": {
           "smtp_server": "localhost",
           "smtp_port": 1025,
           "smtp_use_tls": false,
           "smtp_username": "your-email@protonmail.com",
           "smtp_password": "your-bridge-password-here",
           "from_email": "your-email@protonmail.com"
       }
   }
   ```

**Security Note**: The `email_config.json` file is in `.gitignore` and will not be committed to Git. Keep this file secure and don't share it.

#### Option B: Using Environment Variables

Set the following environment variables before starting PrivacyBot:

```bash
export EMAIL_PROVIDER=smtp
export SMTP_SERVER=localhost
export SMTP_PORT=1025
export SMTP_USE_TLS=false
export SMTP_USERNAME=your-email@protonmail.com
export SMTP_PASSWORD=your-bridge-password-here
export FROM_EMAIL=your-email@protonmail.com
```

For permanent configuration, add these to your `.bashrc`, `.zshrc`, or create a `.env` file.

### 3. Test the Configuration

Run the test script to verify your configuration:

```bash
cd app
python3 test_smtp_config.py
```

This will test:
- Configuration loading
- Environment variable support
- SMTP connection (if Bridge is running)

### 4. Run PrivacyBot

Follow the standard PrivacyBot installation instructions in the README.md. When you run the application:

1. Make sure Proton Mail Bridge is running
2. Start the Flask server: `flask run`
3. Start the React application: `npm start`
4. Use PrivacyBot as normal - emails will be sent through ProtonMail

## Troubleshooting

### Connection Refused Error
- **Problem**: Cannot connect to SMTP server
- **Solution**: 
  - Ensure Proton Mail Bridge is running
  - Check that the SMTP port is correct (usually 1025)
  - Try using `127.0.0.1` instead of `localhost`

### Authentication Failed
- **Problem**: SMTP authentication fails
- **Solution**:
  - Verify you're using the Bridge password, not your ProtonMail password
  - Check Bridge settings to view/regenerate the Bridge password
  - Ensure your username is correct (usually your full email address)

### TLS/SSL Errors
- **Problem**: TLS handshake errors
- **Solution**:
  - For Proton Mail Bridge, set `smtp_use_tls` to `false`
  - Bridge uses a local connection that doesn't require TLS

### Emails Not Sending
- **Problem**: No error but emails don't appear in sent folder
- **Solution**:
  - Check Bridge application logs
  - Verify your ProtonMail account is active
  - Check if you've reached ProtonMail's sending limits

## Reverting to Gmail API

To switch back to the Gmail API method:

1. Change the configuration file:
   ```json
   {
       "email_provider": "gmail_api"
   }
   ```

2. Or set environment variable:
   ```bash
   export EMAIL_PROVIDER=gmail_api
   ```

## Security Considerations

1. **Never commit credentials**: The `email_config.json` file is gitignored
2. **Bridge password**: Keep your Bridge password secure
3. **Local only**: Proton Mail Bridge only accepts connections from localhost
4. **No OAuth required**: SMTP method doesn't require browser-based OAuth flows

## Advantages of Using Proton Mail Bridge

1. **Privacy**: ProtonMail offers end-to-end encryption
2. **No OAuth**: Simpler authentication without browser redirects
3. **Standard SMTP**: Works like any other email provider
4. **Local security**: Bridge handles encryption/decryption locally

## Support

For Proton Mail Bridge issues:
- ProtonMail Support: https://protonmail.com/support
- Bridge Documentation: https://protonmail.com/bridge/install

For PrivacyBot issues:
- Check the main README.md
- Review the GitHub repository
