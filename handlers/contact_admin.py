from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

keyboard = ReplyKeyboardMarkup(
    [["🔙 Back"]],
    resize_keyboard=True,
)

async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
☎️ CONTACT ADMIN

━━━━━━━━━━━━━━━━━━

Telegram
@YOUR_USERNAME

Phone
080XXXXXXXX

Hours
8:00 AM - 8:00 PM

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=keyboard,
    )

contact_admin_handler = MessageHandler(
    filters.Regex(r"^☎️ Contact Admin$"),
    contact_admin,
)