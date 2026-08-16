from telegram import ReplyKeyboardMarkup


def main_menu_keyboard():
    keyboard = [
        ["📋 Available Plans"],
        ["📊 My Usage", "👤 My Account"],
        ["💳 Billing", "📞 Support"],
        
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )