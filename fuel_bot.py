import requests
import os

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]
API_KEY = os.environ["EIA_API_KEY"]


def get_fuel_price():

    url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={API_KEY}&frequency=weekly&data[0]=value&facets[product][]=JF&facets[area][]=USGC&sort[0][column]=period&sort[0][direction]=desc&length=1"

    r = requests.get(url)
    data = r.json()

    price = float(data["response"]["data"][0]["value"])

    return price


def calc_fedex(price):

    if price < 2.8:
        return 35.0
    elif price < 3.0:
        return 38.5
    elif price < 3.2:
        return 41.5
    else:
        return 45.0


def calc_dhl(price):

    if price < 2.8:
        return 28.0
    elif price < 3.0:
        return 30.5
    elif price < 3.2:
        return 33.0
    else:
        return 35.0


def send_slack(text):

    requests.post(
        SLACK_WEBHOOK,
        json={"text": text}
    )


price = get_fuel_price()

fedex = calc_fedex(price)
dhl = calc_dhl(price)

msg = f"""
Jet Fuel Price
{price} USD/gallon

燃油サーチャージ（推定）

FedEx {fedex}%
DHL   {dhl}%
"""

send_slack(msg)
