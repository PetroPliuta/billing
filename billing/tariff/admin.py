from django.contrib import admin
from .models import InternetTariff
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from billing.helpers import is_one_list_in_another_list


class InternetTariffAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'download_speed_kbps', 'upload_speed_kbps', 'price', 'view_customers'
    list_display_links = 'title', 'download_speed_kbps', 'upload_speed_kbps', 'price'
    ordering = 'id',

    def save_model(self, request, obj, form, change):
        if change and is_one_list_in_another_list(('download_speed_kbps', 'upload_speed_kbps'), form.changed_data):
            customers = obj.customer_set.all()
        super().save_model(request, obj, form, change)
        if change and is_one_list_in_another_list(('download_speed_kbps', 'upload_speed_kbps'), form.changed_data):
            for customer in customers:
                customer.coa()

    def view_customers(self, obj):
        count = obj.customer_set.count()
        url = (
            reverse("admin:customer_customer_changelist")
            + "?"
            + urlencode({"tariff__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} customer(s)</a>', url, count)

    view_customers.short_description = "Customers"


admin.site.register(InternetTariff, InternetTariffAdmin)
