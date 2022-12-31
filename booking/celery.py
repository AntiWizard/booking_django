import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking.settings')
app = Celery('booking')

app.conf.timezone = 'ASIA/Tehran'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_raservation': {
        'task': 'hotel.tasks.check_raservation',
        'schedule': crontab(minute="*"),
    },
}
