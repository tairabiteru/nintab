import typing as t


WEEKDAYS = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]


def convert_to_seconds(number: int, unit: str) -> int:
    if "minute" in unit:
        number *= 60
    elif "hour" in unit:
        number *= 3600
    elif "day" in unit:
        number *= 86400
    elif "week" in unit:
        number *= (86400 * 7)
    elif "year" in unit:
        number *= (86400 * 365)
    return number


def convert_to_time_tuple(time_string: str) -> t.Tuple[int, int, int]:
    try:
        h, m, s = tuple(time_string.split(":"))
    except ValueError:
        h, m = tuple(time_string.split(":"))
        s = "00"

    h, m, s = map(int, (h, m, s))
    return h, m, s