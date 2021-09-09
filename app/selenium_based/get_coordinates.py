from typing import Dict, Any
import time

from .utils import get_driver
from ..common import parameters, parse_strings, round_coordinates

import helium as he


def process(profile: Dict[str, str]) -> Dict[str, str]:
    with get_driver() as driver:
        he.set_driver(driver)
        he.go_to(parameters.LATLONG_URL)

        search_box = he.find_all(he.S("#searchboxinput"))[0]

        source_url = driver.current_url

        he.write(profile["residence"], into=search_box)
        he.press(he.ENTER)

        he.wait_until(lambda: source_url != driver.current_url, timeout_secs=15)
        time.sleep(5)

        url = driver.current_url

        longitude_raw, latitude_raw = url.split("/")[6].split(",")[:2]
        longitude = parse_strings(longitude_raw)
        latitude = parse_strings(latitude_raw)

        profile_updated = profile.copy()
        profile_updated["longitude"] = round_coordinates(longitude)
        profile_updated["latitude"] = round_coordinates(latitude)

    return profile_updated
