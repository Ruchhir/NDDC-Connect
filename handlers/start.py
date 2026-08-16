from keyboards import main_menu_keyboard

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database import get_user, create_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_user = update.effective_user

    existing_user = get_user(telegram_user.id)

    if existing_user is None:
        create_user(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name
        )

        print(f"✅ New user: {telegram_user.first_name}")

    else:
        print(f"👋 Welcome back: {telegram_user.first_name}")

    await update.message.reply_text(
        f"""🌐 NDDC Hostel Connect

Fast • Secure • Unlimited

━━━━━━━━━━━━━━━━━━

🏠 Welcome, {telegram_user.first_name}! 👋

Choose an option below.
""",
        reply_markup=main_menu_keyboard()
    )


start_handler = CommandHandler("start", start)