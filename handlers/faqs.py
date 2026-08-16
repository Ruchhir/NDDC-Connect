from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

keyboard = ReplyKeyboardMarkup(
    [["🔙 Back"]],
    resize_keyboard=True,
)

async def faqs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
❓ FREQUENTLY ASKED QUESTIONS

━━━━━━━━━━━━━━━━━━

• How do I connect after payment?

• Payment successful but no internet?

• Can I use multiple devices?

• How do I contact support?

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=keyboard,
    )

faqs_handler = MessageHandler(
    filters.Regex(r"^❓ FAQs$"),
    faqs,
)