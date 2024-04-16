
from celery import Celery
from core.config import settings



celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.conf.timezone = 'US/Eastern'