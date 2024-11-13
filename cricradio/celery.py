from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cricradio.settings')

app = Celery('cricradio')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule a periodic task
app.conf.beat_schedule = {
    'run-my-scheduled-task': {
        'task': 'match.tasks.my_scheduled_task',  # Ensure this task is defined correctly
        'schedule': crontab(minute='*/1'),  # Runs every 1 minute
    },
}

# This is necessary to make sure the app is available
# when importing from 'cricradio' elsewhere.
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Worker pool for Windows (solo pool)
app.conf.update(
    worker_pool='solo',  # Use the solo pool for Windows (if on Windows)
)
