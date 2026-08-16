import os
from dotenv import load_dotenv

from telegram.ext import Application

from database import initialize_database
from handlers.start import start_handler
from handlers.plans import plans_handler
from handlers.order import order_handler
from handlers.checkout import checkout_handler
from handlers.payments import payments_handler
from handlers.multiple_devices import multiple_devices_handler
from handlers.premium import premium_handler
from handlers.usage import usage_handler
from handlers.account import account_handler
from handlers.billing import billing_handler
from handlers.support import support_handler
from handlers.subscription import subscription_handler
from handlers.back import back_handler
from handlers.report_issue import report_issue_handler
from handlers.contact_admin import contact_admin_handler
from handlers.faqs import faqs_handler
from handlers.verify import verify_handler


# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found.")
        return

    initialize_database()
    print("✅ Database initialized.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(plans_handler)
    app.add_handler(order_handler)
    app.add_handler(checkout_handler)
    app.add_handler(payments_handler)
    app.add_handler(verify_handler)
    app.add_handler(multiple_devices_handler)
    
    app.add_handler(premium_handler)
    app.add_handler(usage_handler)
    app.add_handler(account_handler)
    app.add_handler(billing_handler)
    app.add_handler(support_handler)
    app.add_handler(subscription_handler)
    app.add_handler(back_handler)
    app.add_handler(report_issue_handler)
    app.add_handler(contact_admin_handler)
    app.add_handler(faqs_handler)
    print("🤖 Bot is running...")
    app.run_polling(
    poll_interval=1,
    timeout=30,
)


if __name__ == "__main__":
    main()

