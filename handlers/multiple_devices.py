from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

keyboard = ReplyKeyboardMarkup(
    [
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def multiple_devices(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📱 MULTIPLE DEVICES

━━━━━━━━━━━━━━━━━━

Want to sub on more than one device?

Shared Access will allow multiple
registered devices to use a single
subscription.

Examples

• Phone + Laptop
• Phone + Tablet
• Temporary Access (Roommates)

━━━━━━━━━━━━━━━━━

🚧 Coming Soon (V.2)

This feature is currently under
development, will be available in
the next update!


""",
        reply_markup=keyboard,
    )


multiple_devices_handler = MessageHandler(
    filters.Regex(r"^❓ Multiple Devices$"),
    multiple_devices,
)