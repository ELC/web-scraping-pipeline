
def parse_strings(string: str) -> float:
    return float(string.strip("@,"))


def round_coordinates(coordinate: float) -> float:
    return round(coordinate * 1e2) * 1e-2
