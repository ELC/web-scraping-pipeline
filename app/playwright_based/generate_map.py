import time
from typing import Dict
import asyncio

from ..common import parameters

from playwright.async_api import async_playwright


async def process(geojson: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(parameters.MAP_URL)

        for _ in range(100):
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Delete")

        await page.keyboard.type(geojson)

        await page.keyboard.press("F11")

        await page.click('[title="Collapse"]')
        await asyncio.sleep(0.5)
        await page.click('[title="Collapse"]')
        await asyncio.sleep(0.5)
        await page.click('[title="Collapse"]')

        await asyncio.sleep(0.5)

        await page.screenshot(path=str(parameters.DATA_PATH / "richest_playwright.png"))
