from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')

app = Celery('djangocrud')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()