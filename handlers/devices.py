from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

devices_keyboard = ReplyKeyboardMarkup(
    [
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def my_devices(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📱 MY DEVICES

━━━━━━━━━━━━━━━━━━

No registered devices.

Your connected devices will
appear here after your first
successful WiFi login.

━━━━━━━━━━━━━━━━━━

🚧 Coming Soon
""",
        reply_markup=devices_keyboard,
    )


devices_handler = MessageHandler(
    filters.Regex(r"^📱 My Devices$"),
    my_devices,
)