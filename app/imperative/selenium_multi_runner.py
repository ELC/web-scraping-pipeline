import json

from mpire import WorkerPool
from tenacity import retry, stop_after_attempt, stop_after_delay

from ..common import clean_data, convert_to_geo_json

from ..common.parameters import MAX_ATTEMPS, PROFILE_COUNT

from ..selenium_based import (
    compile_profile,
    process_profile,
    generate_map,
    get_coordinates,
)

from ..tests.create_test import test_agains_expected

stop_criterion = stop_after_attempt(MAX_ATTEMPS)

clean_data.delete_data = retry(clean_data.delete_data, stop=stop_criterion)
compile_profile.compile_profiles = retry(
    compile_profile.compile_profiles,
    stop=(stop_criterion | stop_after_delay(20 * MAX_ATTEMPS)),
)
process_profile.process = retry(
    process_profile.process, stop=(stop_criterion | stop_after_delay(120))
)
generate_map.process = retry(
    generate_map.process, stop=(stop_criterion | stop_after_delay(120))
)
get_coordinates.process = retry(
    get_coordinates.process, stop=(stop_criterion | stop_after_delay(120))
)
convert_to_geo_json.process = retry(
    convert_to_geo_json.process, stop=(stop_criterion | stop_after_delay(20))
)


def process(profile):
    profile_residence = process_profile.process(profile)
    return get_coordinates.process(profile_residence)


def runner():
    clean_data.delete_data()
    profiles = compile_profile.compile_profiles()
    assert test_agains_expected(PROFILE_COUNT, "profiles", profiles)

    args = [{"profile": profile} for profile in profiles]

    with WorkerPool(n_jobs=5) as pool:
        profiles_with_coordinates = pool.map_unordered(
            process, args, iterable_len=len(profiles)
        )
    assert test_agains_expected(
        PROFILE_COUNT, "profiles_with_coordinates", profiles_with_coordinates
    )

    geojson = convert_to_geo_json.process(profiles_with_coordinates)
    assert test_agains_expected(PROFILE_COUNT, "geojson", json.loads(geojson))

    return generate_map.process(geojson)
