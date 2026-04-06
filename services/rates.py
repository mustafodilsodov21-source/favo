import requests

def get_usd():
    data = requests.get("https://open.er-api.com/v6/latest/USD").json()
    return round(data["rates"]["UZS"], 2)

def convert_currency(amount: float, currency: str):
    data = requests.get(f"https://open.er-api.com/v6/latest/{currency}").json()
    rate = data["rates"]["UZS"]
    return round(amount * rate, 2)