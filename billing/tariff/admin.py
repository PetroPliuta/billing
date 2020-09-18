from django.contrib import admin
from .models import InternetTariff


class InternetTariffAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'download_speed_kbps', 'upload_speed_kbps', 'price'
    list_display_links = 'title', 'download_speed_kbps', 'upload_speed_kbps', 'price'
    ordering = 'id',


admin.site.register(InternetTariff, InternetTariffAdmin)
