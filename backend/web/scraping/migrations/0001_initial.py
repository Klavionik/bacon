# Generated by Django 4.2.2 on 2023-06-16 22:47

from django.db import migrations, models
import web.scraping.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrypoint', models.CharField(choices=[('scrapers.PerekrestokScraper', 'scrapers.PerekrestokScraper')], max_length=256)),
                ('config', web.scraping.models.TOMLField(blank=True)),
            ],
        ),
    ]
