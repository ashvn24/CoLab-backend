from __future__ import absolute_import,unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')

app = Celery('backend')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings,namespace='CELERY')

#beat settings

# app.conf.beat_schedule = {
#     'delete-old-accepted-requests': {
#         'task': 'users.task.delete_old_accepted_requests',
#         'schedule': timedelta(seconds=5),  # Run the task every 5 seconds
#     },
# }


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    