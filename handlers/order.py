from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

from database import get_all_plans

continue_keyboard = ReplyKeyboardMarkup(
    [
        ["💳 Continue to Checkout"],
        ["🔙 Back"],
    ],
    resize_keyboard=True,
)


async def order_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    # Save selected plan
    context.user_data["plan_id"] = chosen_plan["id"]

    # Icons
    icons = {
        "Lite": "🚀",
        "Daily": "🌅",
        "Weekly": "📅",
        "Premium Plus": "⭐",
    }

    icon = icons.get(chosen_plan["name"], "📶")

    display_name = "Monthly" if chosen_plan["name"] == "Premium Plus" else chosen_plan["name"]

    hours = chosen_plan["duration_hours"]

    if hours < 24:
        duration = f"{hours} Hours"
    elif hours == 24:
        duration = "24 Hours"
    elif hours == 720:
        duration = "30 Days"
    else:
        duration = f"{hours // 24} Days"

    await update.message.reply_text(
        f"""
🧾 ORDER SUMMARY

━━━━━━━━━━━━━━━━━━

{icon} {display_name}

💰 Price
₦{chosen_plan['price']:,}

⏱ Duration
{duration}

📶 Speed
Unlimited

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=continue_keyboard,
    )


order_handler = MessageHandler(
    filters.Regex(r"^(🚀|🌅|📅|⭐) "),
    order_summary,
)