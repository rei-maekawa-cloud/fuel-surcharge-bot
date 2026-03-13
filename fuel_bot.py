import requests
import re
import os

url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)

matches = re.findall(r"\d+\.\d+%", res.text)

fuel = "取得失敗"

if matches:
    fuel = matches[0]

webhook = os.environ["SLACK_WEBHOOK"]

msg = {
    "text": f"FedEx燃油サーチャージ\n{fuel}"
}

requests.post(webhook, json=msg)
