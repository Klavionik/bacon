# Generated by Django 4.2.2 on 2023-06-27 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_scraper_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='entrypoint',
            field=models.CharField(choices=[('web.scraping.providers.PerekrestokProvider', 'web.scraping.providers.PerekrestokProvider')], max_length=256),
        ),
    ]
