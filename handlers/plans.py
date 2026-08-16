from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_all_plans


async def available_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):

    plans = get_all_plans()

    keyboard = []

    icons = {
        "Lite": "🚀",
        "Daily": "🌅",
        "Weekly": "📅",
        "Premium Plus": "⭐",
    }

    message = """
📋 AVAILABLE PLANS

━━━━━━━━━━━━━━━━━━
"""

    for plan in plans:

        icon = icons.get(plan["name"], "📶")

        display_name = (
            "Monthly"
            if plan["name"] == "Premium Plus"
            else plan["name"]
        )

        keyboard.append([f"{icon} {display_name}"])

    keyboard.append(["❓ Multiple Devices"])
    keyboard.append(["🔙 Back"])

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
    )


plans_handler = MessageHandler(
    filters.Regex(r"^📋 Available Plans$"),
    available_plans,
)