import requests
import os

# -----------------------
# Fuel Index取得
# -----------------------

def get_fuel_price():

    url = "https://api.eia.gov/v2/petroleum/pri/spt/data/?frequency=weekly&data[0]=value&facets[product][]=JF&facets[area][]=USGC&sort[0][column]=period&sort[0][direction]=desc&length=1"

    r = requests.get(url)

    data = r.json()

    price = data["response"]["data"][0]["value"]

    return float(price)


# -----------------------
# FedEx計算
# -----------------------

def calc_fedex(price):

    if price < 2.40: return 30
    if price < 2.60: return 33
    if price < 2.80: return 35
    if price < 3.00: return 38.5
    if price < 3.20: return 41
    if price < 3.40: return 44

    return 47


# -----------------------
# DHL計算
# -----------------------

def calc_dhl(price):

    if price < 2.40: return 24
    if price < 2.60: return 26
    if price < 2.80: return 28
    if price < 3.00: return 30.5
    if price < 3.20: return 33
    if price < 3.40: return 35

    return 38


# -----------------------
# main
# -----------------------

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

webhook = os.environ["SLACK_WEBHOOK"]

requests.post(
    webhook,
    json={"text": msg}
)
