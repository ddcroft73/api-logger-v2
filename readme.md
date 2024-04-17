

## API Logger V2

A logger designed for user based web API systems. Logs events for each user independantly. Uses a robust task queue system, Celery to make certain no system, or user log is ever missed no matter how big, or busy your backend is.  Very simple operation and setup. It operates and logs data under a "stream" system. Streams are nothing more than a file that holds a certin type of log entry, and you can add or delete your own streams. The default streams are:

* INFO
* WARN
* DEBUG
* LOGIN
* ERROR
* SECURITY ALERT
* STRANGE ACTIVITY
* INTERNAL

Internal is just what it sounds like and is automatic. it is how any error or message from within the logger is handled.  This is the only one that needs to be left as is, but I have had issues with it in the past. I'm trying to figure out how I can keep it because it is necessary. So You can see the default interface is a lot like any other logger but it works totally different. You dont need to worry about levels and only being able to log certain levels at certain times or altogether.  If you want to log INFO, you simply set that as the "stream" and give it your message. ERROR, same. Below is a simple example of how to use it in a python application.

```python
from app.logger.celery_app import logger
from datatime import datetime, timezone

# The first 3 args are postional, after that they are all Kwargs.
logger.delay(
    Stream,     # "INFO", "ERROR", or any other stream
    Location,   # Username or "system"
    Message, 
    **kwargs    # tinmestamp, heading, dict_to_string, m
)

# If you call it with no positionals, and just an "m" kwarg:
# This will result in a system INFO stream message
logger.delay(m="This log entry will go under INFO for the system.")

logger.delay("INFO", current_active_user, "Log entry here.", timestamp=True)
logger.delay("ERROR", "system", "Log entry here.", timestamp=True)

# Results:
# a simple one line log entry.
INFO:  Log entry here. § [2024-04-09 20:39:05]


# This allows you to log your entry in JSON (Sort of) format. Some entries are just better read this way and it allows
# you better control over the data. 
user_data_dict = {
    "username": "usera1@gizzleMail.com",
    "IP_Address": "200.88.45.102",
    "time_in":  datetime.now(timezone.utc)
}

logger.delay(
    "LOGIN",                         # stream
    user_data_dict.get("username"),  # The user to log it under
    user_data_dict,                  # THe dictionary
    dict_to_string=True,             # This tells it to format like JSON, else it will be one line
    heading="New Login",             # Optional heading over the readout.
)

#Results:
LOGIN: New Login
{
    "username": "usera1@gizzleMail.com",
    "ip_address": "200.88.45.102",
    "time_in": "04/09/2024 21:08:10",
}
```




# The Idea

I happened upon this project while building the backend to another project. I have yet to finish that project because I fell in love with this logger.  [V1](https://github.com/ddcroft73/api-logger) was simple and a lot like this one still except for how the core logging works. I wanted to make it asynchronous. I had to becasue in a busy backend you could very easily miss log entries due to simultaneous logging.  That was the main issue with V1. As is, it is a fantastic little logger to keep all your entries separated and there is a nice archiving feature that this version also shares. So I set out to make it asynchronous with the notion in the back of my head that this was going to be difficult to make sure it never misses anything. I mean anything at all. Then i t hit me. Celery! What a perfect use case for Celery! All I'd have to do is a few tweaks to the code and if the project already uses Celery even better! Just add a task for loggging with a special interface and all set!  And if it doesn't use Celery it woudn't be difficult to generate tthe files and code necessary to get it  working and embed the code in the loggers directory. The user wouldn't even need to be aware of it at all.... So I started building this. CLI installer that either adds a task to an existing celery app or intalls anc implements it's own app for the purpose. I went a bit farther with this becaus I want to make it as easy to use as possible. It is tailored to user based systems promarilty, but can be set up to just support system logs. It will keep separate logs for each user. The premise is, everyting done on the system is tied to a user, more or less, so log any errors or info under the user that was using the app at the time. Its also a great way to track what each user is doing and to catch nefarious doings.
