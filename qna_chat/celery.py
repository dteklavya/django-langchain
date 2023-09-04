import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_langchain.settings")

app = Celery("django_langchain")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
