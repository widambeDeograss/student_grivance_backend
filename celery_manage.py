# celery_manage.py
from django.utils import timezone
from celery import Celery
from django.conf import settings

app = Celery('student_grivance_backed')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configure periodic tasks
app.conf.beat_schedule = {
    'check-time-limit-notifications': {
        'task': 'your_app.tasks.check_time_limit_notifications',
        'schedule': timezone.timedelta(minutes=1),  # Example: check every 5 minutes
    },
}
