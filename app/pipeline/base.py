from typing import List, Dict, Any

import warnings

from ..common import convert_to_geo_json, clean_data as clean

from ..common.parameters import MAX_ATTEMPS

from dagster import (
    solid,
    RetryPolicy,
    Nothing,
    ExperimentalWarning,
)

warnings.filterwarnings("ignore", category=ExperimentalWarning)

SOLID_COMMON_PARAMS = {"retry_policy": RetryPolicy(max_retries=MAX_ATTEMPS, delay=30)}


@solid(**SOLID_COMMON_PARAMS)
def clean_data() -> Nothing:
    clean.delete_data()


@solid(**SOLID_COMMON_PARAMS)
def convert_geojson(profiles: List[Dict[str, Any]]) -> str:
    return convert_to_geo_json.process(profiles)
