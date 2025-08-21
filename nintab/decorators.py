import datetime
import re
import typing as t


REGEX = {
    'unit': r"(seconds?|minutes?|hours?|days?|weeks?|months?|years?){1}",
    'weekday': r"((sun|mon|tues|wednes|thurs|fri|satur)days?){1}",
    'int': r"\d+",
    'time': r"([0-1]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?",
    'season': r"(spring)|(summer)|(autumn)|(fall)|(winter){1}"
}


def construct_cron_string(cron_format: str) -> t.Tuple[str, t.List[str]]:
    patterns: t.List[str] = []
    in_regex = False
    current = ""

    for char in cron_format:
        if in_regex is True:
            if char == "}":
                in_regex = False
                patterns.append(REGEX[current])
                current = ""
            else:
                current += char
        else:
            if char == "{":
                in_regex = True
            
    for key, regex in REGEX.items():
        key = "{" + key + "}"

        if key in cron_format:
            cron_format = cron_format.replace(key, regex)
    
    return cron_format, patterns


def scheduler(cron_format: str):
    crontab, patterns = construct_cron_string(cron_format)
    scheduler.crontab = crontab

    def inner(func):
        def wrapper(*args, **kwargs):
            match = re.search(crontab, args[0])
            
            if not match:
                raise ValueError(f"Input string '{args[0]}' does not match format '{cron_format}'")
            
            arguments = []
            input_string = args[0]
            for pattern in patterns:
                match = re.search(pattern, input_string)
                input_string = re.sub(pattern, "", input_string, count=1)
                arguments.append(match.group())
            
            now = kwargs.get("now", datetime.datetime.now())
            return func(now, *arguments)
        wrapper.crontab = scheduler.crontab
        return wrapper
    
    inner.crontab = scheduler.crontab
    return inner