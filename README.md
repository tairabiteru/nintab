# Nintab - Cron for humans
Nintab is a little scheduling library I wrote that allows you to run things on a schedule using easy to understand, human readable strings.

## Examples
The following will print `hi` every 5 seconds:
```Python
import nintab


@nintab.schedule("every 5 seconds")
def my_function():
    print("hi!")


if __name__ == "__main__":
    my_function()
```
Coroutines also work. You can also handle the specifics of the loop yourself by using `get_future()`:
```Python
import datetime
import nintab


now = datetime.datetime.now()

# Returns a datetime which satisfies the string.
# Ex,  if it were August 20th 2025, 17:00, it 
# would return August 26th 2025, 10:00.
future = nintab.get_future("every tuesday at 10:00", now=now)
```
## Installation
Requires Python >=3.10:
```
pip install git+https://github.com/tairabiteru/nintab.git
```
## FAQ
- **Why?**
  - I know there's other scheduling libraries out there, but I wanted to write my own for fun. That's kind of all there is to it.
- **What's the name mean?**
  - "nin" (pronounced *neen*) comes from Japanese, specifically the *On* reading of the character 人. The character itself means "people." "Tab" from cron*tab*. Nintab. "People tab."

