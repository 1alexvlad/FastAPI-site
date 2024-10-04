from celery import Celery


celery = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    include=['tasks.tasks']
)

celery.conf.broker_connection_retry_on_startup = True