import requests
from bs4 import BeautifulSoup
import json
import os

# Slack Webhook
SLACK_WEBHOOK = "YOUR_SLACK_WEBHOOK_URL"

# キャッシュ保存
CACHE_FILE = "fuel_cache.json"


def send_slack(message):
    requests.post(
        SLACK_WEBHOOK,
        json={"text": message}
    )


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)


# -------------------------
# FedEx燃油サーチャージ取得
# -------------------------
def get_fedex_fuel():

    url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    # 1行目（最新）
    first = rows[1].find_all("td")

    period = first[0].text.strip()
    fuel = first[2].text.strip()

    return {
        "period": period,
        "fuel": fuel
    }


# -------------------------
# DHL燃油サーチャージ取得
# -------------------------
def get_dhl_fuel():

    url = "https://www.dhl.com/global-en/home/express/shipping/surcharges.html"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text()

    import re
    match = re.search(r"\d+\.\d+%", text)

    if match:
        fuel = match.group()
    else:
        fuel = "unknown"

    return {
        "fuel": fuel
    }


# -------------------------
# メイン処理
# -------------------------
def main():

    cache = load_cache()

    fedex = get_fedex_fuel()
    dhl = get_dhl_fuel()

    new_data = {
        "fedex": fedex["fuel"],
        "dhl": dhl["fuel"]
    }

    messages = []

    if cache.get("fedex") != fedex["fuel"]:
        messages.append(
            f"FedEx燃油サーチャージ更新\n{cache.get('fedex')} → {fedex['fuel']}\n期間: {fedex['period']}"
        )

    if cache.get("dhl") != dhl["fuel"]:
        messages.append(
            f"DHL燃油サーチャージ更新\n{cache.get('dhl')} → {dhl['fuel']}"
        )

    if messages:
        send_slack("\n\n".join(messages))

    save_cache(new_data)


if __name__ == "__main__":
    main()
