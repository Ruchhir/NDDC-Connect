from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

support_keyboard = ReplyKeyboardMarkup(
    [
        ["📩 Report Issue"],
        ["☎️ Contact Admin"],
        ["❓ FAQs"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📞 SUPPORT CENTER

━━━━━━━━━━━━━━━━━━

Need help?

Choose one of the options below.

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=support_keyboard,
    )


support_handler = MessageHandler(
    filters.Regex(r"^📞 Support$"),
    support,
)