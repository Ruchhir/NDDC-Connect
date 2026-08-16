from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

shared_keyboard = ReplyKeyboardMarkup(
    [
        ["2 Devices"],
        ["3 Devices"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def shared_access(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["access_type"] = "Shared"

    await update.message.reply_text(
        """
👥 Shared Access

━━━━━━━━━━━━━━━━━━

Select the number of devices.
""",
        reply_markup=shared_keyboard,
    )


shared_access_handler = MessageHandler(
    filters.Regex("^Shared Access$"),
    shared_access,
)