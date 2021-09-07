import json
from typing import List, Dict

from ..common.parameters import PROFILE_COUNT
from ..tests.create_test import test_agains_expected


def process(profiles: List[Dict[str, str]]) -> str:

    assert test_agains_expected(PROFILE_COUNT, "profiles_with_coordinates", profiles)

    points = []

    for profile in profiles:
        point = (profile["latitude"], profile["longitude"])
        points.append(point)

    geojson = {"type": "MultiPoint", "coordinates": points}

    geojson_string = json.dumps(geojson)

    assert test_agains_expected(PROFILE_COUNT, "geojson", json.loads(geojson_string))

    return geojson_string
