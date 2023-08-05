from django.contrib import admin

from web.notifications.models import TelegramSubscription

admin.site.register(TelegramSubscription)
