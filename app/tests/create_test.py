import json
from pathlib import Path


def save_data(count, /, **kwargs):
    destination = Path("app", "tests", str(count))
    destination.mkdir(parents=True, exist_ok=True)

    for parameter, value in kwargs.items():
        with open(destination / f"{parameter}.json", "w") as json_file:
            json.dump(value, json_file, indent=4)


def test_agains_expected(count, parameter, value):
    source = Path("app", "tests", str(count))

    json_file_path = source / f"{parameter}.json"

    if not json_file_path.exists():
        kwargs = {parameter: value}
        save_data(count, **kwargs)
        return True

    with open(json_file_path) as json_file:
        expected = json.load(json_file)

    return value == expected
