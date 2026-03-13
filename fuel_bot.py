import asyncio
import os
import re
import requests
from playwright.async_api import async_playwright


async def get_fedex(page):

    url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"

    await page.goto(url)

    # テーブルが表示されるまで待つ
    await page.wait_for_selector("table")

    text = await page.inner_text("body")

    matches = re.findall(r"\d{2}\.\d+%", text)

    for m in matches:

        v = float(m.replace("%",""))

        if 20 < v < 60:
            return m

    return None


async def get_dhl(page):

    url = "https://mydhl.express.dhl/jp/ja/ship/surcharges.html#/fuel_surcharge"

    await page.goto(url)

    await page.wait_for_timeout(4000)

    text = await page.inner_text("body")

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
