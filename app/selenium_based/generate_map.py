import time

from .utils import get_driver, get_headless_driver
from ..common import parameters

import helium as he


def process(geojson: str) -> None:
    with get_driver() as driver:
        he.set_driver(driver)
        he.go_to(parameters.MAP_URL)

        text_area = he.find_all(he.S(".CodeMirror"))[0]
        he.click(text_area)

        he.press([he.BACK_SPACE] * 100)
        he.press([he.DELETE] * 100)
        he.press(geojson)

        he.click(he.find_all(he.S(".collapse-button"))[0])

        time.sleep(0.2)

        driver.save_screenshot(str(parameters.DATA_PATH / "richest_selenium.png"))
