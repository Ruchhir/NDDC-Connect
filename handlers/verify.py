from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

from database import (
    get_transaction,
    mark_transaction_paid,
)

from services.paystack import verify_transaction


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/verify REFERENCE"
        )
        return

    reference = context.args[0]

    transaction = get_transaction(reference)

    if transaction is None:
        await update.message.reply_text(
            "❌ Transaction not found."
        )
        return

    response = verify_transaction(reference)

    print("=" * 60)
    print("VERIFY RESPONSE")
    print(response)
    print("=" * 60)

    if not response.get("status"):
        await update.message.reply_text(
            "❌ Unable to verify payment."
        )
        return

    data = response["data"]

    if data["status"] == "success":

        mark_transaction_paid(reference)

        await update.message.reply_text(
            f"""
✅ PAYMENT VERIFIED

━━━━━━━━━━━━━━━━━━

🧾 Reference
{reference}

💰 Amount
₦{transaction["amount"]:,}

📦 Status
Successful

━━━━━━━━━━━━━━━━━━

Your payment has been confirmed.
"""
        )

    else:

        await update.message.reply_text(
            f"""
⌛ PAYMENT STATUS

━━━━━━━━━━━━━━━━━━

Reference
{reference}

Status
{data['status'].title()}

━━━━━━━━━━━━━━━━━━

Payment has not been completed.
"""
        )


verify_handler = CommandHandler(
    "verify",
    verify,
)