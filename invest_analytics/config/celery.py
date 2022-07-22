import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-currency-rates': {
        'task': 'market.tasks.update_currency_courses',
        'schedule': crontab('*/2')
    },
    'update-stock-last-prices': {
        'task': 'market.tasks.update_stock_last_prices',
        'schedule': crontab('*/5')
    }
}