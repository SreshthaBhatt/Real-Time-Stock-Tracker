from __future__ import unicode_literals,absolute_import
import os
from celery import Celery
from django.conf import settings
from celery import shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE','stockproject.settings')

app=Celery('stockproject')

app.conf.enable_utc=False
app.conf.update(timezone='Aisa/Kolkata')

app.config_from_object(settings,namespace='CELERY')

app.conf.beat_schedule={
    'every-10-seconds':{
        'task':'app.tasks.update_stock',
        'schedule':10,
        'args':(['RELIANCE.NS','BHARTIARTL.NS'],)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')