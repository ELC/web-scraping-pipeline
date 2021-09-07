from typing import Dict, Any
import json

from dagster import (
    pipeline,
    solid,
    Nothing,
    DynamicOutputDefinition,
    ModeDefinition,
    fs_io_manager,
    DynamicOutput,
    InputDefinition,
)

from ..selenium_based import (
    compile_profile,
    generate_map,
    get_coordinates,
    process_profile,
)

from .base import SOLID_COMMON_PARAMS, clean_data, convert_geojson

from ..common.parameters import PROFILE_COUNT
from ..tests.create_test import test_agains_expected

# Dynamic
@solid(
    input_defs=[InputDefinition("delete", Nothing)],
    output_defs=[DynamicOutputDefinition(Dict[str, str])],
    **SOLID_COMMON_PARAMS
)
def compile_profile_list_selenium() -> Dict[str, str]:
    profiles = compile_profile.compile_profiles()
    assert test_agains_expected(PROFILE_COUNT, "profiles", profiles)
    for profile in profiles:
        mapping_key = str(hash(str(profile)))[-7:]
        yield DynamicOutput(profile, mapping_key=mapping_key)


@solid(**SOLID_COMMON_PARAMS)
def add_residence_selenium(profile: Dict[str, str]) -> Dict[str, str]:
    return process_profile.process(profile)


@solid(**SOLID_COMMON_PARAMS)
def add_coordinates_selenium(profile: Dict[str, str]) -> Dict[str, Any]:
    return get_coordinates.process(profile)


@solid(**SOLID_COMMON_PARAMS)
def geojson_to_map_selenium(geojson: str) -> Nothing:
    return generate_map.process(geojson)


@pipeline(mode_defs=[ModeDefinition(resource_defs={"io_manager": fs_io_manager})])
def selenium_pipeline():
    data_cleaned = clean_data()
    profiles = compile_profile_list_selenium(delete=data_cleaned)

    profile_with_residence = profiles.map(add_residence_selenium)
    profile_with_coordinates = profile_with_residence.map(add_coordinates_selenium)

    geojson = convert_geojson(profile_with_coordinates.collect())

    geojson_to_map_selenium(geojson)
