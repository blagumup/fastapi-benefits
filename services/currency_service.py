
import requests
from fastapi import HTTPException
from config import get_settings

settings = get_settings()

def convert_currency(currency: str, summ: float):
    """
    Convert a given amount from any currency to USD using NBU rates.
    """
    rates = get_nbu_rates()

    # ✅ Ensure we have exchange rates for both the requested currency and USD
    if currency.upper() not in rates:
        print(f"❌ Error: Requested currency {currency.upper()} not found in rates.")
        raise HTTPException(status_code=400, detail=f"Invalid currency code: {currency.upper()}")

    if "USD" not in rates:
        print("❌ Error: USD rate unavailable in NBU rates.")
        raise HTTPException(status_code=400, detail="USD rate unavailable in exchange rates.")

    currency_val = rates[currency.upper()]
    usd_to_uah = rates["USD"]

    usd_value = (summ * currency_val) / usd_to_uah  # Direct conversion

    return {
        "currency": currency.upper(),
        "original_amount": summ,
        "converted_to_usd": round(usd_value, 2)
    }


def get_nbu_rates():
    """Fetch exchange rates from the National Bank of Ukraine (NBU)."""
    response = requests.get(settings.NBU_API_URL)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch exchange rates from NBU")

    rates = {rate['cc']: rate['rate'] for rate in response.json()}
    
    # ✅ Add UAH manually since it's not included in NBU API
    rates["UAH"] = 1.0  # 1 UAH = 1 UAH
    
    return rates
