from flask import session, redirect, url_for
from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    render_template,
)

import uuid
import os
import hmac
import hashlib
import sqlite3

from datetime import datetime, timedelta, UTC

from database import (
    get_plan,
    create_transaction,
    get_transaction,
    mark_transaction_paid,
)

from services.paystack import (
    initialize_transaction,
    verify_transaction,
)

from services.mikrotik import authorize_mac


app = Flask(__name__)
app.secret_key = "nddc-super-secret-key"
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")


# =====================================================
# HOME / CAPTIVE PORTAL
# =====================================================

@app.route("/")
def index():
    return send_file("portal.html")


# =====================================================
# CREATE PAYMENT
# =====================================================

@app.route("/api/create-payment", methods=["POST"])
def create_payment():

    data = request.get_json()

    plan_id = data.get("plan_id")
    mac_address = data.get("mac_address", "PENDING")

    if not plan_id:
        return jsonify({
            "success": False,
            "message": "Plan ID is required"
        })

    plan = get_plan(plan_id)

    if not plan:
        return jsonify({
            "success": False,
            "message": "Invalid plan"
        })

    amount = plan["price"] * 100

    reference = f"NDDC-{uuid.uuid4().hex[:10].upper()}"

    response = initialize_transaction(
        email="student@example.com",
        amount=amount,
        reference=reference,
    )

    if not response.get("status"):
        return jsonify({
            "success": False,
            "message": "Unable to initialize payment"
        })

    # Save transaction
    create_transaction(
        telegram_id=0,
        plan_id=plan_id,
        reference=reference,
        amount=plan["price"],
        mac_address=mac_address,
    )

    return jsonify({
        "success": True,
        "checkout_url": response["data"]["authorization_url"]
    })


# =====================================================
# PAYSTACK WEBHOOK
# =====================================================

@app.route("/paystack/webhook", methods=["POST"])
def paystack_webhook():

    print("🔥 WEBHOOK HIT")

    signature = request.headers.get("x-paystack-signature")

    body = request.get_data()

    expected_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode(),
        body,
        hashlib.sha512,
    ).hexdigest()

    # Verify signature
    if signature != expected_signature:
        return jsonify({
            "status": False,
            "message": "Invalid signature"
        }), 401

    payload = request.get_json()

    # Ignore non-payment events
    if payload.get("event") != "charge.success":
        return jsonify({"status": True}), 200

    reference = payload["data"]["reference"]

    print("=" * 50)
    print("PAYMENT RECEIVED")
    print("Reference:", reference)

    # Find transaction
    transaction = get_transaction(reference)

    if not transaction:
        print("Transaction not found.")
        return jsonify({"status": False}), 404

    # Prevent duplicate processing
    if transaction["status"] == "success":
        print("Transaction already processed.")
        return jsonify({"status": True}), 200

    # Verify with Paystack
    response = verify_transaction(reference)

    if not response.get("status"):
        print("Verification failed.")
        return jsonify({"status": False}), 400

    payment = response["data"]

    if payment["status"] != "success":
        print("Payment not successful.")
        return jsonify({"status": False}), 400

    # Get the purchased plan
    plan = get_plan(transaction["plan_id"])

    # Calculate expiry time
    expires_at = (
        datetime.now(UTC) +
        timedelta(hours=plan["duration_hours"])
    )

    # Mark transaction paid
    mark_transaction_paid(reference)

    # Save expiry time
    conn = sqlite3.connect("data/wifi.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET expires_at = ?
        WHERE reference = ?
    """, (
        expires_at.strftime("%Y-%m-%d %H:%M:%S"),
        reference,
    ))

    conn.commit()
    conn.close()

    # Activate the device
    authorize_mac(
        mac_address=transaction["mac_address"],
        duration_hours=plan["duration_hours"],
    )

    print("PAYMENT VERIFIED SUCCESSFULLY")
    print("Expires at:", expires_at)
    print("=" * 50)

    return jsonify({"status": True}), 200


# =====================================================
# PAYMENT SUCCESS PAGE
# =====================================================

@app.route("/payment/success")
def payment_success():

    reference = request.args.get("reference")

    if not reference:
        return "Invalid payment reference"

    transaction = get_transaction(reference)

    if not transaction:
        return "Transaction not found"

    return f"""
    <html>
    <head>
        <title>NDDC Connect</title>

        <style>
            body {{
                background:#0d1117;
                color:white;
                font-family:Arial,sans-serif;
                display:flex;
                justify-content:center;
                align-items:center;
                min-height:100vh;
                margin:0;
            }}

            .card {{
                background:#161b22;
                border:1px solid #30363d;
                border-radius:18px;
                padding:32px;
                width:90%;
                max-width:420px;
                text-align:center;
            }}

            .check {{
                font-size:64px;
                margin-bottom:16px;
            }}

            .amount {{
                font-size:32px;
                color:#f0b90b;
                margin:12px 0;
            }}

            .ref {{
                background:#0f172a;
                padding:12px;
                border-radius:10px;
                margin-top:20px;
                font-size:14px;
                word-break:break-all;
            }}
        </style>
    </head>

    <body>

        <div class="card">

            <div class="check">📡</div>

            <h1>Payment Successful</h1>

            <p>Your internet purchase has been received.</p>

            <div class="amount">
                ₦{transaction["amount"]:,}
            </div>

            <p>We are preparing your connection.</p>

            <div class="ref">
                <strong>Reference:</strong><br>
                {reference}
            </div>

        </div>

    </body>
    </html>
    """


# =====================================================
# MANUAL VERIFY (DEV ONLY)
# =====================================================

@app.route("/verify/<reference>")
def verify_payment(reference):

    transaction = get_transaction(reference)

    if not transaction:
        return "Transaction not found"

    response = verify_transaction(reference)

    if not response.get("status"):
        return "Verification failed"

    payment = response["data"]

    if payment["status"] != "success":
        return f"Payment status: {payment['status']}"

    if transaction["status"] == "success":
        return f"""
        <h1>⚠️ ALREADY VERIFIED</h1>
        <p><strong>Reference:</strong> {reference}</p>
        <p><strong>MAC:</strong> {transaction["mac_address"]}</p>
        """

    plan = get_plan(transaction["plan_id"])

    expires_at = (
        datetime.utcnow() +
        timedelta(hours=plan["duration_hours"])
    )

    mark_transaction_paid(reference)

    conn = sqlite3.connect("data/wifi.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET expires_at = ?
        WHERE reference = ?
    """, (
        expires_at.strftime("%Y-%m-%d %H:%M:%S"),
        reference,
    ))

    conn.commit()
    conn.close()

    authorize_mac(
        mac_address=transaction["mac_address"],
        duration_hours=plan["duration_hours"],
    )

    return f"""
    <h1>✅ PAYMENT VERIFIED</h1>
    <p><strong>Reference:</strong> {reference}</p>
    <p><strong>MAC:</strong> {transaction["mac_address"]}</p>
    <p><strong>Duration:</strong> {plan["duration_hours"]} hours</p>
    <p><strong>Expires At:</strong> {expires_at}</p>
    """


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@app.route("/admin")
def admin_dashboard():

    import sqlite3

    conn = sqlite3.connect("data/wifi.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # ============================================
    # TOTAL REVENUE
    # ============================================
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM transactions
        WHERE status='success'
    """)

    revenue = cursor.fetchone()["total"]


    # ============================================
    # TODAY'S REVENUE
    # ============================================
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM transactions
        WHERE status='success'
          AND date(created_at) = date('now')
    """)

    today_revenue = cursor.fetchone()["total"]


    # ============================================
    # SUCCESSFUL PAYMENTS COUNT
    # ============================================
    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM transactions
        WHERE status='success'
    """)

    payments = cursor.fetchone()["count"]


    # ============================================
    # ACTIVE SESSIONS
    # ============================================
    cursor.execute("""
        SELECT mac_address, amount, expires_at
        FROM transactions
        WHERE status='success'
          AND expires_at IS NOT NULL
          AND expires_at > datetime('now')
        ORDER BY expires_at ASC
    """)

    active_sessions = cursor.fetchall()

    active_devices = len(active_sessions)


    # ============================================
    # RECENT TRANSACTIONS
    # ============================================
    cursor.execute("""
        SELECT reference, amount, status, created_at
        FROM transactions
        ORDER BY created_at DESC
        LIMIT 10
    """)

    transactions = cursor.fetchall()

    conn.close()


    # ============================================
    # RENDER DASHBOARD
    # ============================================
    return render_template(
        "admin.html",
        revenue=revenue,
        today_revenue=today_revenue,
        payments=payments,
        active_devices=active_devices,
        active_sessions=active_sessions,
        transactions=transactions,
    )

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )