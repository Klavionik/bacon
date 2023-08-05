from rest_framework import serializers

from web.notifications import models


class TelegramSubscription(serializers.ModelSerializer):
    class Meta:
        model = models.TelegramSubscription
