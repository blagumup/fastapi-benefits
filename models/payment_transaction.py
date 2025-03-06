from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class PaymentTransaction(BaseModel):
    payer_name: str
    payment_purpose: str
    transaction_date: date
    recipient: str
    currency: str
    amount: Decimal
    address: str
