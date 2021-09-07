from playwright.async_api import async_playwright

from ..common import parameters


async def process(profile):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(profile["profile_url"])

        personal_information = await page.query_selector_all(".profile-stats__item")

        residence_row = None
        for personal_field in personal_information:
            personal_field_text = await personal_field.inner_text()
            if "residence" in personal_field_text.lower():
                residence_row = personal_field
                break

        residence_element = await residence_row.query_selector(".profile-stats__text")
        residence = await residence_element.inner_text()

        profile_updated = profile.copy()
        profile_updated["residence"] = residence

    return profile_updated
