from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_plan

checkout_keyboard = ReplyKeyboardMarkup(
    [
        ["💳 Pay with Paystack"],
        ["🏦 Bank Transfer (Coming Soon)"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):

    plan_id = context.user_data.get("plan_id")

    if not plan_id:
        await update.message.reply_text(
            "❌ No plan selected."
        )
        return

    plan = get_plan(plan_id)

    display_name = (
        "Monthly"
        if plan["name"] == "Premium Plus"
        else plan["name"]
    )

    await update.message.reply_text(
        f"""
💳 CHECKOUT

━━━━━━━━━━━━━━━━━━

📦 Plan
{display_name}

💰 Amount
₦{plan['price']:,}

━━━━━━━━━━━━━━━━━━

Select a payment method.
""",
        reply_markup=checkout_keyboard,
    )


checkout_handler = MessageHandler(
    filters.Regex("^💳 Continue to Checkout$"),
    checkout,
)