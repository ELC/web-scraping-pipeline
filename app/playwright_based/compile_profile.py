from playwright.async_api import async_playwright

from ..common import parameters


async def compile_profiles():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(parameters.BASE_URL)
        await page.click('[aria-label="Open Navigation Menu"]')
        await page.hover("text=Billionaires")
        await page.click("text=World's Billionaires")

        await page.wait_for_selector(".table-row")
        rows = await page.query_selector_all(".table-row")

        first_row = rows[0]
        await first_row.click()

        profiles = []

        for row in rows:
            await row.click()

            full_profile = await page.query_selector("text=Full Profile")
            profile_button = await full_profile.query_selector("xpath=//..")
            profile_url = await profile_button.get_attribute("href")

            person_node = await row.query_selector(".personName")
            name = await person_node.inner_text()

            profile = {"name": name, "profile_url": profile_url}

            profiles.append(profile)

            if len(profiles) >= parameters.PROFILE_COUNT:
                break

        return profiles
