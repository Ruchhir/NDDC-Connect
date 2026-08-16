import uuid

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
)

from database import (
    get_plan,
    create_transaction,
)
from services.paystack import initialize_transaction


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("========== PAY BUTTON ==========")

    plan_id = context.user_data.get("plan_id")
    print("Plan ID:", plan_id)

    if not plan_id:
        await update.message.reply_text(
            "❌ No plan selected."
        )
        return

    plan = get_plan(plan_id)
    print("Plan:", plan)

    # Temporary email (we'll replace this later)
    email = "test@example.com"

    # Paystack expects Kobo
    amount = plan["price"] * 100
    print("Amount:", amount)

    # Generate unique reference
    reference = f"NDDC-{uuid.uuid4().hex[:10].upper()}"
    print("Reference:", reference)

    # Initialize Paystack transaction
    response = initialize_transaction(
        email=email,
        amount=amount,
        reference=reference,
    )

    print("Paystack Response:", response)

    if not response.get("status"):
        await update.message.reply_text(
            "❌ Unable to initialize payment."
        )
        return

    # Save transaction after successful initialization
    create_transaction(
        telegram_id=update.effective_user.id,
        plan_id=plan_id,
        reference=reference,
        amount=plan["price"],   # Stored in Naira
    )

    payment_url = response["data"]["authorization_url"]

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🌐 Pay Now",
                    url=payment_url,
                )
            ]
        ]
    )

    display_name = (
        "Monthly"
        if plan["name"] == "Premium Plus"
        else plan["name"]
    )

    await update.message.reply_text(
        f"""
💳 PAYMENT

━━━━━━━━━━━━━━━━━━

📦 Plan
{display_name}

💰 Amount
₦{plan['price']:,}

━━━━━━━━━━━━━━━━━━

Click the button below to complete your payment securely through Paystack.
""",
        reply_markup=keyboard,
    )


payments_handler = MessageHandler(
    filters.Regex(r"^💳 Pay with Paystack$"),
    pay,
)