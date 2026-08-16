from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

subscription_keyboard = ReplyKeyboardMarkup(
    [
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
🧾 SUBSCRIPTION

━━━━━━━━━━━━━━━━━━

📶 Active Plan
None

📅 Start Date
--

⏰ Expiry Date
--

🟢 Status
Inactive

━━━━━━━━━━━━━━━━━━

Purchase a WiFi plan to activate
your subscription.
""",
        reply_markup=subscription_keyboard,
    )


subscription_handler = MessageHandler(
    filters.Regex(r"^🧾 Subscription$"),
    subscription,
)