# Generated by Django 4.2.2 on 2023-06-21 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.FloatField()),
                ('old', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256)),
                ('url', models.URLField(unique=True)),
                ('in_stock', models.BooleanField(null=True)),
                ('meta', models.JSONField(blank=True, default=dict)),
                ('processing_status', models.CharField(choices=[('pending', 'Pending'), ('done', 'Done'), ('error', 'Error')], default='pending', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('display_title', models.CharField(max_length=64)),
                ('product_url_pattern', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('external_id', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.store')),
            ],
        ),
    ]
