import os
import base64
import datetime
import requests
from flask import Flask, request, jsonify
from requests.auth import HTTPBasicAuth
from flask_cors import CORS  # For handling CORS requests

app = Flask(__name__)
CORS(app)  # Allow all origins (Customize in production)

# Load MPESA Credentials from Environment Variables
CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
BUSINESS_SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")  # Default to 174379 for testing
PASSKEY = os.getenv("MPESA_PASSKEY")
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL", "https://yourbackend.com/mpesa/callback")

# Function to get access token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token: {e}")
        return None

# Function to send STK Push
@app.route("/mpesa/stkpush", methods=["POST", "OPTIONS"])
def stk_push():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight request successful"}), 200

    data = request.json
    phone_number = data.get("phone")
    amount = data.get("amount")

    if not phone_number or not amount:
        return jsonify({"error": "Phone number and amount are required"}), 400

    # Validate phone number format
    if phone_number.startswith("07"):
        phone_number = "254" + phone_number[1:]
    elif not phone_number.startswith("254") or len(phone_number) != 12:
        return jsonify({"error": "Invalid phone number format"}), 400

    # Get access token
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    # Generate timestamp & password
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "DemoPayment",
        "TransactionDesc": "Ticket Payment Demo",
    }

    try:
        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error making STK push request: {e}")
        return jsonify({"error": "Failed to send STK push request"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "False") == "True")
