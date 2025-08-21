import datetime

from .decorators import scheduler
from .utils import convert_to_seconds, convert_to_time_tuple, WEEKDAYS


@scheduler("every {int} {unit}")
def every_int_unit(now: datetime.datetime, number=None, unit=None) -> datetime.datetime:
    if "month" in unit:
        raise ValueError(f"'month(s)' cannot be used with this scheduler because they are an ill defined period of time.")
    
    number = int(number)
    number = convert_to_seconds(number, unit)
    delta = datetime.timedelta(seconds=number)
    return now + delta


@scheduler("every {int} {unit} at {time}")
def every_int_unit_at_time(now=None, number=None, unit=None, time=None) -> datetime.datetime:
    if "month" in unit:
        raise ValueError(f"'month(s)' cannot be used with this scheduler because they are an ill defined period of time.")
    if any([u in unit for u in ["second", "minute", "hour"]]):
        raise ValueError(f"Units like 'hours', 'minutes', or 'seconds' cannot be used with this scheduler.")
    
    number = int(number)
    number = convert_to_seconds(number, unit)
    
    delta = datetime.timedelta(seconds=number)
    now += delta
    
    h, m, s = convert_to_time_tuple(time)

    now = now.replace(hour=h, minute=m, second=s)
    return now


@scheduler("every {weekday} at {time}")
def every_weekday_at_time(now=None, weekday=None, time=None) -> datetime.datetime:
    while now.date().weekday() != WEEKDAYS.index(weekday):
        now += datetime.timedelta(days=1)
    
    h, m, s = convert_to_time_tuple(time)
    future = now.replace(hour=h, minute=m, second=s)

    if now > future:
        now += datetime.timedelta(days=7)

    now = now.replace(hour=h, minute=m, second=s)
    return now


@scheduler("on {weekday} at {time}")
def on_weekday_at_time(weekday=None, time=None) -> datetime.datetime:
    return every_weekday_at_time(f"every {weekday} at {time}")


@scheduler("every month on day {int} at {time}")
def every_month_on_day_int_at_time(now=None, day=None, time=None) -> datetime.datetime:
    day = int(day)
    h, m, s = convert_to_time_tuple(time)
    
    if now.date().day == day:
        future = now.replace(hour=h, minute=m, second=s)
        if future > now:
            return future
    
    next_month = now.date().month + 1
    if next_month == 13:
        next_month = 1
    
    now = now.replace(month=next_month, day=day, hour=h, minute=m, second=s)
    return now


schedulers = [
    every_int_unit,
    every_int_unit_at_time,
    every_weekday_at_time,
    every_month_on_day_int_at_time,
    on_weekday_at_time
]