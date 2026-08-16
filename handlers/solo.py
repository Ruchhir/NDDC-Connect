from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def solo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["access_type"] = "Solo"
    context.user_data["device_limit"] = 1

    await update.message.reply_text(
        "⏳ Preparing your order..."
    )


solo_handler = MessageHandler(
    filters.Regex("^Solo$"),
    solo,
)