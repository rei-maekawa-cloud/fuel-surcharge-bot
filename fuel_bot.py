import requests
from bs4 import BeautifulSoup
import os

url = "https://www.fedex.com/en-us/shipping/rates/fuel-surcharge.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

fuel = "取得失敗"

tables = soup.find_all("table")

for table in tables:
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            if "%" in cols[1].text:
                fuel = cols[1].text.strip()
                break

webhook = os.environ["SLACK_WEBHOOK"]

msg = {
    "text": f"FedEx燃油サーチャージ\n{fuel}"
}

requests.post(webhook, json=msg)
