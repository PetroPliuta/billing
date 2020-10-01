from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Customer, Transaction
from .forms import CustomerForm
import copy
from billing.helpers import format_mac, is_mac, is_one_list_in_another_list
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.utils.html import format_html


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'login',  'tariff', 'ip_address',
                    'balance', 'active', 'online')
    list_display_links = ('login',)
    list_editable = ('ip_address', 'active', 'tariff')
    list_filter = ('active', 'online')
    readonly_fields = ('online', 'balance', 'last_online_datetime',
                       'last_online_ip', 'last_online_router', 'last_online_dhcp')
    save_as = True
    save_as_continue = False
    search_fields = ('login', 'ip_address')
    ordering = ("id",)
    form = CustomerForm

    def save_model(self, request, obj, form, change):
        def is_disconnect_needed():
            return change and (is_one_list_in_another_list(('login', 'password', 'ip_address'), form.changed_data) or
                               ('active' in form.changed_data and not obj.active))
        if is_disconnect_needed():
            try:
                old_object = self.model.objects.get(id=obj.id)
            except Exception as ex:
                print("Cannot get old object:", ex)
        if is_mac(obj.login):
            old_login = obj.login
            obj.login = format_mac(old_login)
            if old_login != obj.login:
                messages.add_message(
                    request, messages.WARNING, f"Login '{old_login}' was changed to '{obj.login}' because it is MAC address.")
        super().save_model(request, obj, form, change)
        if is_disconnect_needed():
            old_object.disconnect()
        elif not obj.tariff or obj.tariff.id != form.initial['tariff']:
            obj.coa()

    def delete_model(self, request, obj):
        customer = copy.copy(obj)
        super().delete_model(request, obj)
        customer.disconnect()

    def delete_queryset(self, request, queryset):
        customers = copy.copy(queryset)
        queryset.delete()
        for obj in customers:
            obj.disconnect()


admin.site.register(Customer, CustomerAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = 'id', 'customer_', 'amount', 'date_time', 'system'
    list_display_links = 'id', 'amount', 'date_time'
    list_filter = 'customer',
    ordering = 'id',
    readonly_fields = 'system', 'date_time'

    def customer_(self, obj):
        url = (
            reverse_lazy("admin:customer_customer_change",
                         args=(obj.customer.id,))
        )
        return format_html('Customer: <a href="{}">{}</a>', url, obj.customer.login)

    customer_.short_description = "Customer"


admin.site.register(Transaction, TransactionAdmin)
admin.site.unregister(Group)
