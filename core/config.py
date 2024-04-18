from dataclasses import dataclass

@dataclass
class Settings:
    PROJECT_NAME: str = "API-Logger V2"    
    CELERY_BROKER_URL: str ="redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str ="redis://redis:6379/0"
    
    # These may remain hard coded... in the api_logger, but Not sure.
    LOG_DIRECTORY: str = "./logs" 
    LOG_ARCHIVE_DIRECTORY: str = f"{LOG_DIRECTORY}/log-archives"
    DEFAULT_LOG_FILE: str = f"{LOG_DIRECTORY}/DEFAULT-app-logs.log"  

    USERS_DIRECTORY: str = f"{LOG_DIRECTORY}/users"
    SYSTEM_DIRECTORY: str = f"{LOG_DIRECTORY}/sys"  # Not sure about this.

settings = Settings()


#
#   A very basic representation of the logging directories for useres and System
#
# logs/
#    |
#    --users/
#    |    |
#    |    --userone@gmail.com
#    |    |           |
#    |    |           ---INFO_log.log
#    |    |           |
#    |    |           ---WARN_log.log  # etc, etc 
#    |    |
#    |    ---userTwo@gmail.com
#    |                |
#    |                ---INFO_log.log
#    |                |
#    |                ---WARN_log.log  # etc, etc 
#    |
#    --sys/
#       |
#       ---INFO_log.log
#       |
#       ---WARN_log.log  # etc, etc