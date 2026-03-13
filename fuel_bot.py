import asyncio
import os
import re
import requests
from playwright.async_api import async_playwright


# -----------------------
# FedEx（API取得）
# -----------------------
def get_fedex():

    url = "https://www.fedex.com/apps/fedextrack/api/surcharge/v1/fuelsurcharge"

    try:
        r = requests.get(url, timeout=10)

        text = r.text

        match = re.search(r"\d{2}\.\d+%", text)

        if match:
            return match.group()

    except:
        pass

    return None


# -----------------------
# DHL
# -----------------------
async def get_dhl(page):

    url = "https://mydhl.express.dhl/jp/ja/ship/surcharges.html#/fuel_surcharge"

    await page.goto(url)

    await page.wait_for_timeout(5000)

    text = await page.inner_text("body")

    matches = re.findall(r"\d{2}\.\d+%", text)

    for m in matches:

        v = float(m.replace("%",""))

        if 20 < v < 50:
            return m

    return None


async def main():

    fedex = get_fedex()

    async with async_playwright() as p:

        browser = await p.chromium.launch()

        page = await browser.new_page()

        dhl = await get_dhl(page)

        await browser.close()

    msg = f"""
燃油サーチャージ

FedEx {fedex}
DHL   {dhl}
"""

    webhook = os.environ["SLACK_WEBHOOK"]

    requests.post(
        webhook,
        json={"text": msg}
    )


asyncio.run(main())
