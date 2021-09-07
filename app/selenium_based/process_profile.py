from .utils import get_driver, get_headless_driver

import helium as he


def process(profile):
    with get_driver() as driver:
        he.set_driver(driver)
        he.go_to(profile["profile_url"])

        personal_information = he.find_all(he.S(".profile-stats__item"))

        residence_row = None
        for personal_field in personal_information:
            if "residence" in personal_field.web_element.text.lower():
                residence_row = personal_field.web_element
                break

        residence = residence_row.find_element_by_class_name("profile-stats__text").text

        profile_updated = profile.copy()
        profile_updated["residence"] = residence

    return profile_updated
