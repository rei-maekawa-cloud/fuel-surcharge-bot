import asyncio
import os
import requests
from playwright.async_api import async_playwright


# ----------------
# FedEx
# ----------------
async def get_fedex(page):

    url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"

    await page.goto(url)

    # テーブル表示まで待つ
    await page.wait_for_selector("table")

    rows = await page.locator("table tr").all()

    for r in rows:

        text = await r.inner_text()

        if "%" in text:

            import re

            m = re.search(r"\d{2}\.\d+%", text)

            if m:
                return m.group()

    return None


# ----------------
# DHL
# ----------------
async def get_dhl(page):

    url = "https://mydhl.express.dhl/jp/ja/ship/surcharges.html#/fuel_surcharge"

    await page.goto(url)

    await page.wait_for_timeout(5000)

    text = await page.inner_text("body")

    import re

    matches = re.findall(r"\d{2}\.\d+%", text)

    for m in matches:

        v = float(m.replace("%",""))

        if 20 < v < 50:
            return m

    return None


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch()

        page = await browser.new_page()

        fedex = await get_fedex(page)
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
