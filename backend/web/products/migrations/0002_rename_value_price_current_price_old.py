# Generated by Django 4.2.2 on 2023-06-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price',
            old_name='value',
            new_name='current',
        ),
        migrations.AddField(
            model_name='price',
            name='old',
            field=models.FloatField(null=True),
        ),
    ]