"""
Configuration file for email provider settings.
Supports both Gmail API (OAuth) and SMTP (for Proton Mail Bridge and others).
"""

import os
import json

class EmailConfig:
    """Email configuration class supporting multiple providers."""
    
    def __init__(self, config_file='email_config.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or use defaults."""
        default_config = {
            'email_provider': 'gmail_api',  # Options: 'gmail_api' or 'smtp'
            'smtp_settings': {
                'smtp_server': 'localhost',
                'smtp_port': 1025,  # Default for Proton Mail Bridge
                'smtp_use_tls': False,  # Proton Bridge doesn't use TLS on localhost
                'smtp_username': '',
                'smtp_password': '',
                'from_email': ''
            }
        }
        
        # Try to load from environment variables first
        env_provider = os.environ.get('EMAIL_PROVIDER')
        if env_provider:
            default_config['email_provider'] = env_provider
        
        env_smtp_server = os.environ.get('SMTP_SERVER')
        if env_smtp_server:
            default_config['smtp_settings']['smtp_server'] = env_smtp_server
        
        env_smtp_port = os.environ.get('SMTP_PORT')
        if env_smtp_port:
            default_config['smtp_settings']['smtp_port'] = int(env_smtp_port)
        
        env_smtp_username = os.environ.get('SMTP_USERNAME')
        if env_smtp_username:
            default_config['smtp_settings']['smtp_username'] = env_smtp_username
        
        env_smtp_password = os.environ.get('SMTP_PASSWORD')
        if env_smtp_password:
            default_config['smtp_settings']['smtp_password'] = env_smtp_password
        
        env_from_email = os.environ.get('FROM_EMAIL')
        if env_from_email:
            default_config['smtp_settings']['from_email'] = env_from_email
        
        env_smtp_use_tls = os.environ.get('SMTP_USE_TLS')
        if env_smtp_use_tls:
            default_config['smtp_settings']['smtp_use_tls'] = env_smtp_use_tls.lower() == 'true'
        
        # Try to load from config file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    # Merge file config with defaults
                    default_config.update(file_config)
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
        
        return default_config
    
    def get_email_provider(self):
        """Return the configured email provider."""
        return self.config.get('email_provider', 'gmail_api')
    
    def get_smtp_settings(self):
        """Return SMTP settings."""
        return self.config.get('smtp_settings', {})
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
