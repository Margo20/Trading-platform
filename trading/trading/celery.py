from __future__ import absolute_import

from celery import Celery
import os
from django.conf import settings
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading.settings')
# создадим экземпляр приложения
app = Celery('trading')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.autodiscover_tasks()

# Finally, the debug_task example is a task that dumps its own request information.
# This is using the new bind=True task option introduced in Celery 3.1 to easily
# refer to the current task instance.


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'pick-up-new-offer-every-60-seconds': {
        'task': 'offer.tasks.req',
        'schedule': crontab(minute='*/1')
    }
}
