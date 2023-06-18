# Generated by Django 4.2.2 on 2023-06-18 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scraping', '0001_initial'),
    ]

    operations = [
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
                ('scraper', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='scraping.scraper')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('external_id', models.CharField(max_length=128)),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='products.retailer')),
            ],
        ),
        migrations.CreateModel(
            name='UserStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='products.store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='products', to='products.store'),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.FloatField()),
                ('old', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='products.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='userstore',
            constraint=models.UniqueConstraint(models.F('user'), models.F('store'), name='uniq_user_store'),
        ),
        migrations.AddConstraint(
            model_name='userproduct',
            constraint=models.UniqueConstraint(models.F('user'), models.F('product'), name='uniq_user_product'),
        ),
        migrations.AddConstraint(
            model_name='store',
            constraint=models.UniqueConstraint(models.F('retailer'), models.F('external_id'), name='uniq_retailer'),
        ),
    ]
