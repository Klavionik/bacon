# Generated by Django 4.2.2 on 2023-08-07 00:12

from django.db import migrations
from django_celery_beat.models import PeriodicTask, IntervalSchedule


def add_refresh_products_task(*_args):
    interval, _ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS)
    PeriodicTask.objects.create(
        name="Refresh products",
        task="web.products.tasks.refresh_products",
        interval=interval,
    )


def remove_refresh_products_task(*_args):
    PeriodicTask.objects.filter(task="web.products.tasks.refresh_products").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_add_perekrestok_retailer'),
        ('django_celery_beat', '0018_improve_crontab_helptext')
    ]

    operations = [
        migrations.RunPython(
            add_refresh_products_task,
            reverse_code=remove_refresh_products_task,
        )
    ]