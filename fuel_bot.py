import requests
from bs4 import BeautifulSoup
import os

url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

text = soup.get_text()

fuel = None

for line in text.split("\n"):
    if "%" in line and "燃油" in line:
        fuel = line.strip()
        break

if fuel is None:
    fuel = "取得失敗"

webhook = os.environ["SLACK_WEBHOOK"]

msg = {
    "text": f"FedEx燃油サーチャージ\n{fuel}"
}

requests.post(webhook, json=msg)
