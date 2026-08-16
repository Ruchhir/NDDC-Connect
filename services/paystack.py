import os

import requests
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

HEADERS = {
    "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    "Content-Type": "application/json",
}


def initialize_transaction(email, amount, reference):
    url = "https://api.paystack.co/transaction/initialize"

    payload = {
        "email": email,
        "amount": amount,
        "reference": reference,
    }

    response = requests.post(
        url,
        json=payload,
        headers=HEADERS,
        timeout=30,
    )

    return response.json()

def verify_transaction(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    return response.json()