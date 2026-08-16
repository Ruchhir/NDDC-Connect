from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

account_keyboard = ReplyKeyboardMarkup(
    [
        ["📱 My Devices"],
        ["🧾 Subscription"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    await update.message.reply_text(
        f"""
👤 MY ACCOUNT

━━━━━━━━━━━━━━━━━━

👤 Name
{user.first_name}

🆔 Username
@{user.username if user.username else "Not Set"}

📧 Email
Not Added

📶 Active Plan
No Active Plan

🟢 Status
Active

━━━━━━━━━━━━━━━━━━

Select an option below.
""",
        reply_markup=account_keyboard,
    )


account_handler = MessageHandler(
    filters.Regex(r"^👤 My Account$"),
    my_account,
)