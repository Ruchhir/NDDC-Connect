from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

keyboard = ReplyKeyboardMarkup(
    [["🔙 Back"]],
    resize_keyboard=True,
)

async def report_issue(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📩 REPORT AN ISSUE

━━━━━━━━━━━━━━━━━━

Describe your problem.

This feature will be connected
to support tickets in Version 2.

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=keyboard,
    )

report_issue_handler = MessageHandler(
    filters.Regex(r"^📩 Report Issue$"),
    report_issue,
)