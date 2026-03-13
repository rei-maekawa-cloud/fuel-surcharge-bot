import requests
import re
import os

url = "https://mydhl.express.dhl/jp/ja/ship/surcharges.html#/fuel_surcharge"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)

fuel = "取得失敗"

# %を全部抽出
matches = re.findall(r"\d+\.\d+%", r.text)

if matches:
    fuel = matches[0]

webhook = os.environ["SLACK_WEBHOOK"]

msg = {
    "text": f"DHL燃油サーチャージ\n{fuel}"
}

requests.post(webhook, json=msg)
