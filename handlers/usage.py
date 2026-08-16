from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

usage_keyboard = ReplyKeyboardMarkup(
    [
        ["🔄 Refresh"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def my_usage(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📊 My Usage

━━━━━━━━━━━━━━━━━━

🟢 Status: No Active Plan

📶 Current Plan:
None

📅 Expiry:
--

📱 Connected Devices:
0

⏱ Time Remaining:
--

📈 Data Usage:
Unlimited

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=usage_keyboard,
    )


usage_handler = MessageHandler(
    filters.Regex("^📊 My Usage$"),
    my_usage,
)