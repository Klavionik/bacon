# Generated by Django 4.2.2 on 2023-07-27 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_telegramsubscription_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramsubscription',
            old_name='telegram_id',
            new_name='chat_id',
        ),
    ]
