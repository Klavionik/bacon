# Generated by Django 4.2.2 on 2023-06-12 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraper',
            name='config',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
