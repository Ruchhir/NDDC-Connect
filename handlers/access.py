from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_all_plans

access_keyboard = ReplyKeyboardMarkup(
    [
        ["Solo"],
        ["Shared Access"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):

    selected = update.message.text

    # Remove emoji
    plan_name = selected.split(" ", 1)[1]

    plans = get_all_plans()

    chosen_plan = None

    for plan in plans:
        display_name = "Monthly" if plan["name"] == "Premium Plus" else plan["name"]

        if display_name == plan_name:
            chosen_plan = plan
            break

    if chosen_plan is None:
        await update.message.reply_text("❌ Plan not found.")
        return

    # Save plan information
    context.user_data["plan_id"] = chosen_plan["id"]

    await update.message.reply_text(
        f"""
📦 {plan_name}

━━━━━━━━━━━━━━━━━━

Select Access Type
""",
        reply_markup=access_keyboard,
    )


access_handler = MessageHandler(
    filters.Regex(r"^(🚀|🌅|📅|💎)\s"),
    access,
)