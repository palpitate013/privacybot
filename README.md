# PROJECT NO LONGER SUPPORTED
## As of 9.28.21 this project has been depreciated and Google Oauth verification is not supported. You can still run the tool but you need to setup your own instance of Google Oauth credentials.

# PrivacyBot

PrivacyBot is a simple automated service to initiate CCPA deletion requests with databrokers.

## How It Works
1. PrivacyBot comprises of a React Frontend and a Python Flask Backend web architecture
2. After starting the application, PrivacyBot can send emails using either:
   - **Gmail API (OAuth)** - Original method requiring OAuth authentication with your Gmail account
   - **SMTP** - New method supporting Proton Mail Bridge and other SMTP servers
3. Once configured, depending on the data provided to the Flask API, a CCPA data delete email is drafted and sent to the data brokers chosen. 
4. A confirmation email is sent back to you listing all the databrokers to whom the email was sent. 



## Prerequisites

1. An email account - This is the email from which you will be initiating the data delete requests. PrivacyBot's data deletion process is most effective if this email is the one which you use the most for personal use.
   - **Option A**: A Gmail account (for Gmail API method)
   - **Option B**: Any email account with SMTP access (ProtonMail via Bridge, Gmail, Outlook, etc.)
2. Install Python 3 (https://www.python.org/downloads/)
3. Ensure pip3 is installed (https://pip.pypa.io/en/stable/installing/)
4. Install node https://nodejs.org/en/download/

## Email Provider Configuration

PrivacyBot supports two email sending methods:

### Option A: Gmail API (Original Method)
Requires setting up Google OAuth credentials. See the original documentation below.

### Option B: SMTP (Recommended for ProtonMail Bridge)

#### Using Proton Mail Bridge

1. **Install Proton Mail Bridge**
   - Download from https://protonmail.com/bridge
   - Install and log in with your ProtonMail account
   - Start the Bridge application

2. **Get SMTP Credentials from Bridge**
   - Open Proton Mail Bridge
   - Go to Settings → Your account
   - Note the SMTP server details (typically `localhost` or `127.0.0.1`)
   - Note the SMTP port (typically `1025`)
   - Copy your Bridge username and password

3. **Configure PrivacyBot for SMTP**
   
   Create a file `app/email_config.json` based on `app/email_config.example.json`:
   
   ```json
   {
       "email_provider": "smtp",
       "smtp_settings": {
           "smtp_server": "localhost",
           "smtp_port": 1025,
           "smtp_use_tls": false,
           "smtp_username": "your-protonmail-username",
           "smtp_password": "your-bridge-password",
           "from_email": "your-email@protonmail.com"
       }
   }
   ```
   
   **Alternatively**, you can use environment variables:
   ```bash
   export EMAIL_PROVIDER=smtp
   export SMTP_SERVER=localhost
   export SMTP_PORT=1025
   export SMTP_USERNAME=your-protonmail-username
   export SMTP_PASSWORD=your-bridge-password
   export FROM_EMAIL=your-email@protonmail.com
   export SMTP_USE_TLS=false
   ```

#### Using Other SMTP Providers

For Gmail, Outlook, or other SMTP providers, adjust the settings accordingly:

**Gmail SMTP Example:**
```json
{
    "email_provider": "smtp",
    "smtp_settings": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_use_tls": true,
        "smtp_username": "your-email@gmail.com",
        "smtp_password": "your-app-password",
        "from_email": "your-email@gmail.com"
    }
}
```

**Note**: For Gmail, you'll need to use an App Password, not your regular password.

## Usage - Running PrivacyBot

#### 1. Download zip file from Github Repo and unzip 

#### 2. Open Visual Studio Code and open the “privacybot-private-main” folder 

#### 3. Open split terminal in VS Code (or any two terminals/cmd prompts on your machine). We will be using one terminal to run the Flask app and the other one to run the React app.


### Start the Flask Server 

#### 1. Create and activate a Python Virtual Environment 

The below commands create and activate a virtual environment named "PB_venv". 

`$ python3 -m venv PB_venv` 

`$ source PB_venv/bin/activate`

#### 2. Navigate to `app` folder and install from requirements.txt

`$ cd app`

`$ pip3 install -r requirements.txt`

To confirm required packages are installed - see if “flask_cors” is installed:

`$ pip3 list`

#### 3: Start the Flask App
Run the below commands within the activated virtual environment.

`$ flask run`

The above commands will start the flask application. It can now be accessed through http://127.0.0.1:5000/

Leave this terminal instance as is, and open the second terminal instance. 

### Start the React Application
PFB a step by step list of commands that informs how to install an instance of the React Server. 

#### 1. Run the following commands in the second terminal to navigate to the `app/PB_UI` folder 

`$ cd app`

`$ cd PB_UI`

#### 2. Check to make sure node and npm is correctly installed

`$ node -v`

`$ npm -v`

#### 3. Install the required packages using npm install. Fix any vulnerabilities found. 

`$ npm install`

`$ npm audit fix`

#### 4. Start the React Application by running the below commands. This may take a moment.

`$ npm run build`

`$ npm start`

#### 5. PrivacyBot will now be running on your local machine. 
You will now be able to fill in the required details on the browser form that is opened by the above React commands. Once the required details are filled in and your GMAIL account is authenticated successfully, PrivacyBot will automatically send data deletion requests to the chosen list of data brokers! Yay!

#### 6. Remove access to PrivacyBot from your Gmail account
