from typing import Dict, List

from .utils import get_driver, get_headless_driver
from ..common import parameters

import helium as he


def compile_profiles() -> List[Dict[str, str]]:
    with get_driver() as driver:
        he.set_driver(driver)
        he.go_to(parameters.BASE_URL)

        menu_button = he.find_all(he.S("nav .icon--hamburger"))[0]
        he.click(menu_button)

        billonaries = he.Text("Billionaires")

        he.wait_until(billonaries.exists)
        he.hover(billonaries)

        worlds = he.Text("World's Billionaires")
        he.wait_until(worlds.exists)
        he.click(worlds)

        rows = he.find_all(he.S(".table .table-row"))

        first_row = rows[0]
        he.click(first_row)

        profiles = []

        for row in rows:
            he.click(row)

            profile_button = he.Text("Full Profile")
            he.wait_until(profile_button.exists, interval_secs=0.1)

            name = row.web_element.find_element_by_class_name("personName").text
            profile_url = profile_button.web_element.get_attribute("href")

            profile = {"name": name, "profile_url": profile_url}

            profiles.append(profile)

            if len(profiles) >= parameters.PROFILE_COUNT:
                break

    return profiles
