import asyncio
import datetime
import inspect
import re
import time

from .schedulers import schedulers


def get_future(cron_string: str, now=None) -> datetime.datetime:
    if now is None:
        now = datetime.datetime.now()

    for scheduler in schedulers:
        match = re.search(scheduler.crontab, cron_string)
        if match:
            return scheduler(cron_string, now=now)
    else:
        raise ValueError(f"String '{cron_string}' did not match any schedulers.")


def schedule(cron_string: str):
    def inner(func):

        if inspect.iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                future = get_future(cron_string)
                now = datetime.datetime.now()

                while True:
                    await asyncio.sleep((future - now).total_seconds())
                    await func(*args, **kwargs)
        else:
            def wrapper(*args, **kwargs):
                future = get_future(cron_string)
                now = datetime.datetime.now()
                
                while True:
                    time.sleep((future - now).total_seconds())
                    func(*args, **kwargs)
        
        return wrapper
    return inner

                
