## API Logger V2

A logger designed for user based web API systems. Logs events for each user independantly. Uses a robust task queue system, Celery to make certain no system, or user log is ever missed no matter how big, or busy your backend is.  Very simple operation and setup. It operates and logs data under a "stream" system. Streams are nothing more than a file that holds a certain type of log entry, and you can add or delete your own streams. There will be a CLI stream editor that you can use to add/delete streams as your system requires. The default streams are listed below and remember, the users have their own directory in the `logs` directory under `logs/users/<USERNAME>/` . There will be a file representing each one of the below streams. The premise is every action on the system belongs to either a user, or the system. This way you know who was behind the wheel when an error happens, or You can see who did what when something else happens or goe wrong. ANd you dont need to comb through hundreds of logs to find out  what happened. 

* **INFO** ::  This can really encompass almost anything.  User info, activity, system info, update info. Pretty much anything.
* **WARN** ::  Any type warning you need to log.
* **DEBUG**  :: Exactly what it says. A place to send debugging/troubleshooting code.
* **LOGIN** ::  Anything to do with a user logging in or out. How many attempts they made, the IP they came from, etc, etc...
* **ERROR**  :: Arguably the most useful of all. A place to log any and all errors. This can be expanded on with the Stream editior, or you can just use this one to encompass them all.
* **STRANGE_ACTIVITY**  ::  Anything odd this user has been doing? Any odd happens on the sytem?
* **INTERNAL**  :: This is where the logger will report any internal errors or messages it experiences.
* **PRINT TO SCREEN**  :: Yes you can also print to the screen. This is not a STREAM so to speak, but A method rather that you send to the screen with a stream selected, and a user or system in mind.

Internal is just what it sounds like and is automatic. it is how any error or message from within the logger is handled.  This is the only one that needs to be left as is, but I have had issues with it in the past. I'm trying to figure out how I can keep it because it is necessary. So You can see the default interface is a lot like any other logger but it works totally different. You dont need to worry about levels and only being able to log certain levels at certain times or altogether.  If you want to log INFO, you simply set that as the "stream" and give it your message. ERROR, same. Below is a simple example of how to use it in a python application.

# Basic Usage:

The logger is built off of a singleton class instance. It is instantiated at the bottom of the class definition, and this is where you can set the names of your Stream files.  The come already set with thoughtful default names, archiving is set to True and the max file length is set to 3000 lines.  The code looks like this:

```python
logzz = APILogger_v2( 
    info_filename="INFO_logzz.log", 
    debug_filename="DEBUG_logzz.log", 
    error_filename="ERROR_logzz.log", 
    login_filename="LOGIN_logzz.log", 
    warning_filename="WARN_logzz.log",  
    strange_activity_filename="STRANGE_logzz.log",
    archive_log_files=True,
    log_file_max_size=3000,   
)

# Any changes can be made here before running your API. The first thing the 
# logger will do is set up all the directories, This happens on instantiation,
# and instantiation happens when you inport the logger. THe app is setup so 
# so that Celery and all tasks are primed and redy to go whenever you spin 
# up your API

```

```python

from app.logger.celery_app import logger
from datatime import datetime, timezone

# The first 3 args are postional, after that they are all Kwargs.
logger.delay(
    <stream>,                 # "INFO", "ERROR", or any other stream
    <username> || "system",   # Username or "system"
    <message>,                # Da message.
    <kwargs>                  # tinmestamp, heading, dict_to_string, m
)
# Since the log entries are turned over to Celery, Celery actually puts the 
# task in a queue and executes them in the order they were received, so you 
# don't actually call a method on the logger class. This is abstracted away
# and done by Celery at the right time. Hence the call to "delay()".

# If you call it with no positionals, and just: m="Log entry message here."
# This will result in a system INFO stream message
logger.delay(m="This log entry will go under INFO for the system.")

# Basic Logger usage and entry syntax.
# Log an INFO Stream message for the current active user on the system.
logger.delay("INFO", current_active_user, "Log entry here.", timestamp=True)
# Log an ERROR Stream message for the System. Non user paspefic
logger.delay("ERROR", "system", "Log entry here.", timestamp=True)

# Results:
# a simple one line log entry.
INFO:  Log entry here. § [2024-04-09 20:39:05]    # No mention of the user, 
                                                  # but it willbe in this users 
                                                  # log directory
ERROR:  Log entry here. § [2024-04-09 20:39:05]   # No mention of the System,
                                                  # but stored in the System 
                                                  # log directory.


# This allows you to log your entry in JSON (Sort of) format. Some entries 
# are just better read this way and it allows you better control over the data. 
# Yes this feature is a bit more involved, but it comes naturally once you've 
# done 4,258 of them. joking... But the layout here really is handy for logging 
# detailed data. 

user_data_dict = {
    "username": "usera1@gizzleMail.com",
    "IP_Address": "200.88.45.102",
    "time_in":  datetime.now(timezone.utc)
}

logger.delay(
    "LOGIN",                         # stream
    user_data_dict.get("username"),  # The user to log it under
    user_data_dict,                  # THe dictionary
    dict_to_string=True,             # This tells it to format like JSON.
    heading="New Login",             # Optional heading over the readout.
)

#Results:
LOGIN: New Login
{
    "username": "usera1@gizzleMail.com",
    "ip_address": "200.88.45.102",
    "time_in": "04/09/2024 21:08:10",
}

## Print a messsage to the screen with a stream and user or system in mind:
logger.delay("SCREEN,INFO", <username> || <system>, "Log entry message here.", <kwargs>)
```

# The Idea

I happened upon this project while building the backend to another project. I have yet to finish that project because I fell in love with this logger.  [V1](https://github.com/ddcroft73/api-logger) was simple and a lot like this one still except for how the core logging works. I wanted to make it asynchronous. I had to becasue in a busy backend you could very easily miss log entries due to simultaneous logging.  That was the main issue with V1. As is, it is a fantastic little logger to keep all your entries separated and there is a nice archiving feature that this version also shares. So I set out to make it asynchronous with the notion in the back of my head that this was going to be difficult to make sure it never misses anything. I mean anything at all. Then i t hit me. Celery! What a perfect use case for Celery! All I'd have to do is a few tweaks to the code and if the project already uses Celery even better! Just add a task for loggging with a special interface and all set!  And if it doesn't use Celery it woudn't be difficult to generate tthe files and code necessary to get it  working and embed the code in the loggers directory. The user wouldn't even need to be aware of it at all.... So I started building this. CLI installer that either adds a task to an existing celery app or intalls anc implements it's own app for the purpose. I went a bit farther with this becaus I want to make it as easy to use as possible. It is tailored to user based systems promarilty, but can be set up to just support system logs. It will keep separate logs for each user. The premise is, everyting done on the system is tied to a user, more or less, so log any errors or info under the user that was using the app at the time. Its also a great way to track what each user is doing and to catch nefarious doings.
