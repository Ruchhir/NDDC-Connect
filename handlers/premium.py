from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

premium_keyboard = ReplyKeyboardMarkup(
    [
        ["💳 Pay Now"],
        ["🔗 Upgrade Connection Type"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def premium_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
💎 Premium Unlimited

💰 Price: ₦8,500

♾️ Unlimited Internet

📱 Standard Access (1 Device)

⚡ High-Speed Connection

📅 Valid for 30 Days

⭐ Best Value

━━━━━━━━━━━━━━━━━━

Ready to activate your subscription?
""",
        reply_markup=premium_keyboard,
    )


premium_handler = MessageHandler(
    filters.Regex("^💎 Premium Unlimited$"),
    premium_plan,
)