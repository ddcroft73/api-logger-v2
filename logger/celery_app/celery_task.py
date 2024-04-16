from celery import Task
from .celery_app import celery
from typing import Optional, Any



class LogEntry(Task):
    def on_success(self, retval, task_id, args, kwargs):
        return

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        return

@celery.task(
    name="log_entry_task", base=LogEntry, bind=True, max_retries=3, default_retry_delay=3,
)
def log_entry_task(self, 
    stream: str, 
    username: str, 
    message: str, 
    dict_to_string: bool = False, 
    heading: Optional[str] = None,
    timestamp: bool = False
) -> Any:
    
    def on_retry(exc):
       '''Do what when retrying?'''


    try:
        '''WIP'''
        # Decide what stream is being logged

    except Exception as exc:
        on_retry(exc)
        raise self.retry(exc=exc)
    

#Command to start the worker.
# Write a bash script to start the app and then start the worker.
#   celery -A logger.celery_app.celery_app.celery worker --loglevel=info --logfile=logs/celery.log    