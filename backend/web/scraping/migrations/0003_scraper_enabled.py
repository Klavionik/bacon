# Generated by Django 4.2.2 on 2023-06-22 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_add_perekrestok_scraper'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraper',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
    ]
