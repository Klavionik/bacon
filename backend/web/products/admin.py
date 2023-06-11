from django.contrib import admin

from web.products import models

admin.site.register(models.Retailer)
admin.site.register(models.Store)
admin.site.register(models.Product)
admin.site.register(models.UserProduct)
admin.site.register(models.UserStore)


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]
