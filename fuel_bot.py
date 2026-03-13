import asyncio
import os
import requests
from playwright.async_api import async_playwright

# -----------------------
# FedEx
# -----------------------
async def get_fedex(page):

    url = "https://www.fedex.com/ja-jp/shipping/surcharges.html"

    await page.goto(url)

    text = await page.content()

    import re
    match = re.search(r"\d{2}\.\d+%", text)

    if match:
        return match.group()

    return None


# -----------------------
# DHL
# -----------------------
async def get_dhl(page):

    url = "https://mydhl.express.dhl/jp/ja/ship/surcharges.html#/fuel_surcharge"

    await page.goto(url)

    await page.wait_for_timeout(3000)

    text = await page.content()

    import re
    match = re.search(r"\d{2}\.\d+%", text)

    if match:
        return match.group()

    return None


# -----------------------
# main
# -----------------------
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
