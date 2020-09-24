from django.contrib import admin
from .models import InternetTariff


class InternetTariffAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'download_speed_kbps', 'upload_speed_kbps', 'price'
    list_display_links = 'title', 'download_speed_kbps', 'upload_speed_kbps', 'price'
    ordering = 'id',

    def save_model(self, request, obj, form, change):
        if change:
            customers = obj.customer_set.all()
            old_tariff = self.model.objects.get(id=obj.id)
        super().save_model(request, obj, form, change)
        if change:
            if old_tariff.download_speed_kbps != obj.download_speed_kbps or \
                    old_tariff.upload_speed_kbps != obj.upload_speed_kbps:
                for customer in customers:
                    customer.CoA()


admin.site.register(InternetTariff, InternetTariffAdmin)
