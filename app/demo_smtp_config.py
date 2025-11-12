#!/usr/bin/env python3
"""
Demo script showing how SMTP configuration works with PrivacyBot.
This demonstrates the configuration options without requiring an actual SMTP server.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import EmailConfig

def demo_default_config():
    """Demonstrate default configuration (Gmail API)."""
    print("\n" + "="*60)
    print("DEMO 1: Default Configuration (Gmail API)")
    print("="*60)
    
    config = EmailConfig()
    print(f"Email Provider: {config.get_email_provider()}")
    print("\nThis will use Gmail API with OAuth authentication.")
    print("No SMTP server required.")

def demo_smtp_with_env_vars():
    """Demonstrate SMTP configuration using environment variables."""
    print("\n" + "="*60)
    print("DEMO 2: Proton Mail Bridge with Environment Variables")
    print("="*60)
    
    # Set environment variables
    os.environ['EMAIL_PROVIDER'] = 'smtp'
    os.environ['SMTP_SERVER'] = 'localhost'
    os.environ['SMTP_PORT'] = '1025'
    os.environ['SMTP_USE_TLS'] = 'false'
    os.environ['SMTP_USERNAME'] = 'user@protonmail.com'
    os.environ['SMTP_PASSWORD'] = 'bridge-password-here'
    os.environ['FROM_EMAIL'] = 'user@protonmail.com'
    
    config = EmailConfig()
    smtp_settings = config.get_smtp_settings()
    
    print(f"Email Provider: {config.get_email_provider()}")
    print(f"\nSMTP Configuration:")
    print(f"  Server: {smtp_settings['smtp_server']}")
    print(f"  Port: {smtp_settings['smtp_port']}")
    print(f"  Use TLS: {smtp_settings['smtp_use_tls']}")
    print(f"  Username: {smtp_settings['smtp_username']}")
    print(f"  From Email: {smtp_settings['from_email']}")
    print(f"  Password: {'*' * len(smtp_settings.get('smtp_password', ''))}")
    
    print("\nThis configuration will:")
    print("  1. Connect to Proton Mail Bridge on localhost:1025")
    print("  2. Authenticate with your Bridge credentials")
    print("  3. Send emails through ProtonMail")
    
    # Clean up
    for key in ['EMAIL_PROVIDER', 'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USE_TLS', 
                'SMTP_USERNAME', 'SMTP_PASSWORD', 'FROM_EMAIL']:
        if key in os.environ:
            del os.environ[key]

def demo_smtp_with_config_file():
    """Demonstrate SMTP configuration using config file."""
    print("\n" + "="*60)
    print("DEMO 3: Gmail SMTP with Configuration File")
    print("="*60)
    
    # Simulate config file content
    config_example = {
        "email_provider": "smtp",
        "smtp_settings": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_use_tls": True,
            "smtp_username": "user@gmail.com",
            "smtp_password": "app-password-here",
            "from_email": "user@gmail.com"
        }
    }
    
    print("Configuration file (email_config.json):")
    import json
    print(json.dumps(config_example, indent=2))
    
    print("\nThis configuration will:")
    print("  1. Connect to Gmail SMTP server on smtp.gmail.com:587")
    print("  2. Use STARTTLS for secure connection")
    print("  3. Authenticate with Gmail app password")
    print("  4. Send emails through Gmail")

def demo_switching_providers():
    """Demonstrate how to switch between providers."""
    print("\n" + "="*60)
    print("DEMO 4: Switching Between Email Providers")
    print("="*60)
    
    print("\nTo use Gmail API (default):")
    print("  - Don't create email_config.json, OR")
    print("  - Set 'email_provider': 'gmail_api' in config file, OR")
    print("  - Set EMAIL_PROVIDER=gmail_api environment variable")
    
    print("\nTo use Proton Mail Bridge:")
    print("  - Create email_config.json with SMTP settings, OR")
    print("  - Set EMAIL_PROVIDER=smtp and other SMTP_* env variables")
    
    print("\nTo use any other SMTP provider:")
    print("  - Set appropriate SMTP server, port, and TLS settings")
    print("  - Examples: Gmail SMTP, Outlook SMTP, custom mail server")

def demo_security_notes():
    """Display security considerations."""
    print("\n" + "="*60)
    print("SECURITY NOTES")
    print("="*60)
    
    print("\n1. Configuration File Security:")
    print("   - email_config.json is in .gitignore")
    print("   - Never commit this file to version control")
    print("   - Keep your SMTP passwords secure")
    
    print("\n2. Environment Variables:")
    print("   - Good for deployment environments")
    print("   - Don't expose in logs or error messages")
    print("   - Can be set in .env file (also gitignored)")
    
    print("\n3. Proton Mail Bridge:")
    print("   - Bridge password is different from ProtonMail password")
    print("   - Only accepts connections from localhost")
    print("   - Provides end-to-end encryption")
    
    print("\n4. Gmail SMTP:")
    print("   - Use App Passwords, not your account password")
    print("   - Enable 2FA on your Google account")
    print("   - App passwords can be revoked if compromised")

def main():
    """Run all demos."""
    print("\n" + "="*70)
    print(" "*15 + "PrivacyBot SMTP Configuration Demo")
    print("="*70)
    
    demos = [
        demo_default_config,
        demo_smtp_with_env_vars,
        demo_smtp_with_config_file,
        demo_switching_providers,
        demo_security_notes,
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\nError in demo: {e}")
    
    print("\n" + "="*70)
    print("For full setup instructions, see:")
    print("  - README.md (Quick start)")
    print("  - PROTON_BRIDGE_SETUP.md (Detailed Proton Mail Bridge guide)")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
