import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA_PATH = Path(__file__).resolve().parent.parent / "data"

DATA_PATH.mkdir(exist_ok=True, parents=True)

BASE_URL = "https://www.forbes.com/"

LATLONG_URL = "https://www.google.com/maps/"

MAP_URL = "https://geojson.io/"

PROFILE_COUNT = 1

MAX_ATTEMPS = 3

NEPTUNE_KEY = os.environ["NEPTUNE_KEY"]
