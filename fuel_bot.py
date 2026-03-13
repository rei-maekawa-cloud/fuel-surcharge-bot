import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.environ["SLACK_WEBHOOK"]

url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"

r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")

table = soup.find("table")
row = table.find_all("tr")[1]

cols = row.find_all("td")

period = cols[0].text.strip()
fuel = cols[2].text.strip()

msg = f"FedEx燃油サーチャージ\n{fuel}\n期間:{period}"

requests.post(WEBHOOK,json={"text":msg})
