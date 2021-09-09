from typing import Dict, Any

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

from ..playwright_based import (
    compile_profile,
    process_profile,
    get_coordinates,
    generate_map,
)

from .base import SOLID_COMMON_PARAMS, clean_data, convert_geojson
from ..tests.create_test import test_agains_expected
from ..common.parameters import PROFILE_COUNT


@solid(
    input_defs=[InputDefinition("delete", Nothing)],
    output_defs=[DynamicOutputDefinition(Dict[str, str])],
    **SOLID_COMMON_PARAMS
)
async def compile_profile_list_playwright() -> Dict[str, str]:
    profiles = await compile_profile.compile_profiles()
    assert test_agains_expected(PROFILE_COUNT, "profiles", profiles)
    for profile in profiles:
        mapping_key = str(hash(str(profile)))[-7:]
        yield DynamicOutput(profile, mapping_key=mapping_key)


@solid(**SOLID_COMMON_PARAMS)
async def add_residence_playwright(profile: Dict[str, str]) -> Dict[str, str]:
    return await process_profile.process(profile)


@solid(**SOLID_COMMON_PARAMS)
async def add_coordinates_playwright(profile: Dict[str, str]) -> Dict[str, Any]:
    return await get_coordinates.process(profile)


@solid(**SOLID_COMMON_PARAMS)
async def geojson_to_map_playwright(geojson: str) -> Nothing:
    return await generate_map.process(geojson)


@pipeline(mode_defs=[ModeDefinition(resource_defs={"io_manager": fs_io_manager})])
def playwright_pipeline():
    data_cleaned = clean_data()
    profiles = compile_profile_list_playwright(delete=data_cleaned)

    profile_with_residence = profiles.map(add_residence_playwright)
    profile_with_coordinates = profile_with_residence.map(add_coordinates_playwright)

    geojson = convert_geojson(profile_with_coordinates.collect())

    geojson_to_map_playwright(geojson)
