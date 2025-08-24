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

    now = now.replace(hour=h, minute=m, second=s, microsecond=0)
    return now


@scheduler("everyday at {time}")
def everyday_at_time(now=None, time=None) -> datetime.datetime:
    h, m, s = convert_to_time_tuple(time)
    future = now.replace(hour=h, minute=m, second=s, microsecond=0)
    if future < now:
        future += datetime.timedelta(days=1)
    return future


@scheduler("every {weekday} at {time}")
def every_weekday_at_time(now=None, weekday=None, time=None) -> datetime.datetime:
    h, m, s = convert_to_time_tuple(time)
    future = now.replace(hour=h, minute=m, second=s, microsecond=0)

    if now.date().weekday() == WEEKDAYS.index(weekday):
        if future < now:
            future += datetime.timedelta(days=7)
        return future

    while future.date().weekday() != WEEKDAYS.index(weekday):
        future += datetime.timedelta(days=1)
    
    return future


@scheduler("on {weekday} at {time}")
def on_weekday_at_time(weekday=None, time=None) -> datetime.datetime:
    return every_weekday_at_time(f"every {weekday} at {time}")


@scheduler("every {weekday}")
def every_weekday(now=None, weekday=None) -> datetime.datetime:
    return every_weekday_at_time(f"every {weekday} at 00:00", now=now)


@scheduler("every month on day {int} at {time}")
def every_month_on_day_int_at_time(now=None, day=None, time=None) -> datetime.datetime:
    day = int(day)
    h, m, s = convert_to_time_tuple(time)
    future = now.replace(hour=h, minute=m, second=s, microsecond=0)

    while future.day != day or future < now:
        future += datetime.timedelta(days=1)

    return future


@scheduler("every {int} day of the month")
def every_int_day_of_the_month(now=None, number=None) -> datetime.datetime:
    day = int(number)
    return every_month_on_day_int_at_time(f"every month on day {day} at 00:00")


@scheduler("on the last day of the month at {time}")
def on_the_last_day_of_the_month_at_time(now=None, time=None) -> datetime.datetime:
    LAST_DAY_MONTHS = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Account for leap years
    if now.month == 2:
        try:
            _ = now.replace(day=29)
            last_day = 29
        except ValueError:
            last_day = 28
    else:
        last_day = LAST_DAY_MONTHS[now.month]

    h, m, s = convert_to_time_tuple(time)

    # If the current day is not the last day, this is the
    # same problem as this scheduler.
    if now.day != last_day:
        return every_month_on_day_int_at_time(f"every month on day {last_day} at {time}", now=now)
    
    # Otherwise, it is the last day of the month, and we have
    # to check to see if we've already passed the specified time.
    future = now.replace(hour=h, minute=m, second=s, microsecond=0)
    if future > now:
        return future
    
    # If we have passed it, we have to advance the month by 1.
    # We also have to check to see if we need to advance the year
    # in December.
    next_month = future.month + 1
    if next_month == 13:
        next_month = 1
        year_offset = 1
    else:
        year_offset = 0

    # We can then create a "new now" by setting the day to the next
    # day, which would be the 1st of the following month.
    future = datetime.datetime(year=future.year + year_offset, month=next_month, day=1, hour=0, minute=0)

    # At this point, this condition can be evaluated by the function
    # normally, so we recurse.
    return on_the_last_day_of_the_month_at_time(f"on the last day of the month at {time}", now=future)
    

schedulers = [
    every_int_unit,
    every_int_unit_at_time,
    every_weekday_at_time,
    every_month_on_day_int_at_time,
    on_weekday_at_time,
    everyday_at_time,
    every_weekday,
    every_int_day_of_the_month,
    on_the_last_day_of_the_month_at_time
]