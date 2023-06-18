from django.contrib import admin

from web.products import models

admin.site.register(models.Retailer)
admin.site.register(models.Store)
admin.site.register(models.UserProduct)
admin.site.register(models.UserStore)


@admin.action(description="Refresh product data")
def update_product(modeladmin, request, queryset):
    for product in queryset:
        product.update()


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [update_product]
