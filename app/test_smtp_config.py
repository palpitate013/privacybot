#!/usr/bin/env python3
"""
Simple test script to validate SMTP configuration and email sending functionality.
This script tests the configuration loading and SMTP connection without actually sending emails.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import EmailConfig
import smtplib

def test_config_loading():
    """Test that configuration loads correctly."""
    print("Testing configuration loading...")
    
    # Test default config (Gmail API)
    config = EmailConfig()
    provider = config.get_email_provider()
    print(f"  Default provider: {provider}")
    assert provider in ['gmail_api', 'smtp'], f"Invalid provider: {provider}"
    print("  ✓ Configuration loads successfully")
    
    # Test SMTP settings
    smtp_settings = config.get_smtp_settings()
    print(f"  SMTP settings keys: {list(smtp_settings.keys())}")
    assert 'smtp_server' in smtp_settings
    assert 'smtp_port' in smtp_settings
    print("  ✓ SMTP settings present")
    
    return True

def test_smtp_connection():
    """Test SMTP connection (if configured)."""
    print("\nTesting SMTP connection...")
    
    config = EmailConfig()
    provider = config.get_email_provider()
    
    if provider != 'smtp':
        print("  ⊗ SMTP not configured, skipping connection test")
        print("    To test SMTP, set EMAIL_PROVIDER=smtp environment variable")
        return True
    
    smtp_settings = config.get_smtp_settings()
    smtp_server = smtp_settings.get('smtp_server', 'localhost')
    smtp_port = smtp_settings.get('smtp_port', 1025)
    smtp_use_tls = smtp_settings.get('smtp_use_tls', False)
    
    print(f"  Attempting connection to {smtp_server}:{smtp_port}")
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=5) as server:
            if smtp_use_tls:
                server.starttls()
            print("  ✓ SMTP connection successful")
            return True
    except ConnectionRefusedError:
        print(f"  ⊗ Connection refused to {smtp_server}:{smtp_port}")
        print("    Make sure Proton Mail Bridge (or SMTP server) is running")
        return False
    except Exception as e:
        print(f"  ⊗ SMTP connection failed: {e}")
        return False

def test_environment_variables():
    """Test that environment variables can override config."""
    print("\nTesting environment variable configuration...")
    
    # Set test environment variable
    os.environ['EMAIL_PROVIDER'] = 'smtp'
    os.environ['SMTP_SERVER'] = 'test.example.com'
    os.environ['SMTP_PORT'] = '9999'
    
    config = EmailConfig()
    provider = config.get_email_provider()
    smtp_settings = config.get_smtp_settings()
    
    assert provider == 'smtp', f"Expected 'smtp', got '{provider}'"
    assert smtp_settings['smtp_server'] == 'test.example.com'
    assert smtp_settings['smtp_port'] == 9999
    
    print("  ✓ Environment variables override config correctly")
    
    # Clean up
    del os.environ['EMAIL_PROVIDER']
    del os.environ['SMTP_SERVER']
    del os.environ['SMTP_PORT']
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("PrivacyBot SMTP Configuration Tests")
    print("=" * 60)
    
    tests = [
        test_config_loading,
        test_environment_variables,
        test_smtp_connection,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n⊗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
