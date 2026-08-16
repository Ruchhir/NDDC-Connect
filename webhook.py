import os
import hmac
import hashlib

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from database import (
    get_transaction,
    mark_transaction_paid,
    get_plan,
)

from services.mikrotik import authorize_mac
from services.paystack import verify_transaction

load_dotenv()

app = Flask(__name__)

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")


@app.route("/paystack/webhook", methods=["POST"])
def paystack_webhook():

    signature = request.headers.get("x-paystack-signature")

    body = request.get_data()

    expected_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode(),
        body,
        hashlib.sha512,
    ).hexdigest()

    # Verify webhook signature
    if signature != expected_signature:
        return jsonify({"status": False}), 401

    payload = request.get_json()

    # Ignore non-payment events
    if payload.get("event") != "charge.success":
        return jsonify({"status": True}), 200

    reference = payload["data"]["reference"]

    print("=" * 50)
    print("PAYMENT RECEIVED")
    print("Reference:", reference)

    # Check transaction exists
    transaction = get_transaction(reference)

    if not transaction:
        print("Transaction not found.")
        return jsonify({"status": False}), 404

    # Verify with Paystack
    response = verify_transaction(reference)

    if not response.get("status"):
        print("Verification failed.")
        return jsonify({"status": False}), 400

    payment = response["data"]

    if payment["status"] != "success":
        print("Payment not successful.")
        return jsonify({"status": False}), 400

    # Mark transaction as paid
    mark_transaction_paid(reference)

    # Get purchased plan
    plan = get_plan(transaction["plan_id"])

    # Activate device using the plan duration
    authorize_mac(
    mac_address=transaction["mac_address"],
    duration_hours=plan["duration_hours"],
)

    print("PAYMENT VERIFIED SUCCESSFULLY")
    print("=" * 50)

    return jsonify({"status": True}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
    )