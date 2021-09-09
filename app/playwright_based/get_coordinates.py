import contextlib
from typing import Dict
import asyncio

from ..common import parameters, parse_strings, round_coordinates

from playwright.async_api import async_playwright
from playwright._impl._api_types import TimeoutError


async def process(profile: Dict[str, str]) -> Dict[str, str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(parameters.LATLONG_URL)

        await page.type("#searchboxinput", profile["residence"])

        await page.keyboard.press("Enter")

        await asyncio.sleep(5)

        try:
            await page.wait_for_url("**/place/**data=**")
        except TimeoutError:
            pass

        await asyncio.sleep(5)

        url = page.url

        longitude_raw, latitude_raw = url.split("/")[6].split(",")[:2]
        longitude = parse_strings(longitude_raw)
        latitude = parse_strings(latitude_raw)

        profile_updated = profile.copy()
        profile_updated["longitude"] = round_coordinates(longitude)
        profile_updated["latitude"] = round_coordinates(latitude)

    return profile_updated
