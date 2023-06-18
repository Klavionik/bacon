# Generated by Django 4.2.2 on 2023-06-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_price_old'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available',
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='processing_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('done', 'Done'), ('error', 'Error')], default='pending', max_length=32),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]