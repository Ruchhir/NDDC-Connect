import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
    "Content-Type": "application/json",
}

payload = {
    "email": "test@example.com",
    "amount": 30000,  # ₦300 in kobo
    "reference": f"TEST-{uuid.uuid4().hex[:8]}",
}

response = requests.post(
    "https://api.paystack.co/transaction/initialize",
    headers=headers,
    json=payload,
)

print(response.status_code)
print(response.json())