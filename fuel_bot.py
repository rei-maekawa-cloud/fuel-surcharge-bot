import requests
from bs4 import BeautifulSoup
import os
import json
import re

# --------------------
# DHL取得
# --------------------
def get_dhl():
    url = "https://mydhl.express.dhl/jp/ja/ship/surcharges.html#/fuel_surcharge"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text()

    match = re.search(r"DHL.*?(\d+\.\d+%)", text)

    if match:
        return match.group(1)

    return None


# --------------------
# FedEx取得
# --------------------
def get_fedex():
    url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text()

    match = re.search(r"FedEx.*?(\d+\.\d+%)", text)

    if match:
        return match.group(1)

    return None


dhl = get_dhl()
fedex = get_fedex()

current = {
    "DHL": dhl,
    "FedEx": fedex
}

# --------------------
# 前回データ読み込み
# --------------------
file = "last.json"

if os.path.exists(file):

    with open(file) as f:
        last = json.load(f)

else:

    last = {}

# --------------------
# 差分チェック
# --------------------
changed = False
lines = []

for k,v in current.items():

    old = last.get(k)

    if old != v:

        changed = True

        if old:

            diff = float(v.replace("%","")) - float(old.replace("%",""))

            lines.append(f"{k} {old} → {v} ({diff:+.2f})")

        else:

            lines.append(f"{k} {v}")

# --------------------
# Slack通知
# --------------------
if changed:

    webhook = os.environ["SLACK_WEBHOOK"]

    msg = {
        "text": "燃油サーチャージ更新\n\n" + "\n".join(lines)
    }

    requests.post(webhook, json=msg)

# --------------------
# 保存
# --------------------
with open(file,"w") as f:

    json.dump(current,f)
