from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from keyboards import main_menu_keyboard


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🏠 Home",
        reply_markup=main_menu_keyboard()
    )


back_handler = MessageHandler(
    filters.Regex("^🔙 Back$"),
    back,
)