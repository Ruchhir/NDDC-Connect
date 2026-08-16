from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

billing_keyboard = ReplyKeyboardMarkup(
    [
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def billing(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
💳 PAYMENT HISTORY

━━━━━━━━━━━━━━━━━━

No payments found.

━━━━━━━━━━━━━━━━━━

Your completed payments
will appear here.

""",
        reply_markup=billing_keyboard,
    )


billing_handler = MessageHandler(
    filters.Regex(r"^💳 Billing$"),
    billing,
)