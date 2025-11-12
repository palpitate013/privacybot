# Quick Start: Using PrivacyBot with Proton Mail Bridge

This is a quick 5-minute setup guide for using PrivacyBot with Proton Mail Bridge.

## Prerequisites
- ✅ Proton Mail Bridge installed and running
- ✅ PrivacyBot cloned/downloaded
- ✅ Python 3 and pip3 installed

## Step 1: Get Your Bridge Credentials (2 minutes)

1. Open **Proton Mail Bridge** application
2. Click on your account
3. Go to **Settings** or click the gear icon
4. Note these values:
   - **SMTP Server**: Usually `127.0.0.1` or `localhost`
   - **SMTP Port**: Usually `1025`
   - **Username**: Your ProtonMail email address
   - **Password**: Click "Show password" - this is your Bridge password (NOT your ProtonMail password)

## Step 2: Configure PrivacyBot (1 minute)

Create the file `app/email_config.json`:

```bash
cd app
cp email_config.example.json email_config.json
```

Edit `email_config.json` with your values:

```json
{
    "email_provider": "smtp",
    "smtp_settings": {
        "smtp_server": "localhost",
        "smtp_port": 1025,
        "smtp_use_tls": false,
        "smtp_username": "yourname@protonmail.com",
        "smtp_password": "your-bridge-password-here",
        "from_email": "yourname@protonmail.com"
    }
}
```

**Important**: Replace the values with YOUR Bridge credentials!

## Step 3: Test Configuration (30 seconds)

```bash
cd app
python3 test_smtp_config.py
```

You should see:
```
✓ Configuration loads successfully
✓ SMTP settings present
✓ Environment variables override config correctly
✓ SMTP connection successful

Tests passed: 3/3
✓ All tests passed!
```

If you see connection errors, make sure Proton Mail Bridge is running!

## Step 4: Run PrivacyBot (1 minute)

Follow the normal PrivacyBot setup:

```bash
# Terminal 1: Start Flask server
cd app
pip3 install -r requirements.txt
flask run

# Terminal 2: Start React app
cd PB_UI
npm install
npm start
```

That's it! PrivacyBot will now send emails through ProtonMail. 🎉

## Troubleshooting

**"Connection refused" error**
- Make sure Proton Mail Bridge is running
- Check that the port is 1025 (not 1125 or 1143)

**"Authentication failed" error**
- Use the Bridge password (from Bridge app), not your ProtonMail password
- Copy the password exactly - no extra spaces

**Emails not appearing in sent folder**
- This is normal - check the ProtonMail web interface
- Bridge syncs may take a minute

## Alternative: Environment Variables

Instead of creating `email_config.json`, you can use environment variables:

```bash
export EMAIL_PROVIDER=smtp
export SMTP_SERVER=localhost
export SMTP_PORT=1025
export SMTP_USE_TLS=false
export SMTP_USERNAME=yourname@protonmail.com
export SMTP_PASSWORD=your-bridge-password
export FROM_EMAIL=yourname@protonmail.com

# Then run Flask
flask run
```

## Reverting to Gmail API

To go back to Gmail API, just delete or rename `email_config.json`:

```bash
mv app/email_config.json app/email_config.json.bak
```

Or change it to:
```json
{
    "email_provider": "gmail_api"
}
```

## Need More Help?

- Detailed guide: See `PROTON_BRIDGE_SETUP.md`
- Run demo: `python3 app/demo_smtp_config.py`
- Test config: `python3 app/test_smtp_config.py`
- Original README: See `README.md`

## Security Reminder

✅ `email_config.json` is gitignored - your password is safe
✅ Never commit this file to Git
✅ Bridge password is different from your ProtonMail password

---

**Ready to protect your privacy!** 🔒
