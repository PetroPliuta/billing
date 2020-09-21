from django.contrib import admin
from .models import Customer, Transaction
from .forms import CustomerForm
import copy


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'login',  'tariff', 'ip_address',
                    'balance', 'active', 'online')
    list_display_links = ('login',)
    list_editable = ('ip_address', 'active', 'tariff')
    list_filter = ('active', 'online')
    readonly_fields = ('online', 'balance', 'last_online_datetime',
                       'last_online_ip', 'last_online_router')
    save_as = True
    save_as_continue = False
    search_fields = ('login', 'ip_address', 'email')
    ordering = ("id",)
    form = CustomerForm

    def save_model(self, request, obj, form, change):
        try:
            if change:
                old_object = self.model.objects.get(id=obj.id)
        except Exception as ex:
            print("Cannot get old object:", ex)
        super().save_model(request, obj, form, change)
        if change:
            old_object.disconnect()

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
    list_display = ('id', 'customer', 'amount', 'date_time', 'system')
    list_display_links = ('customer', 'amount')
    list_filter = ('customer',)
    ordering = ("id",)
    readonly_fields = 'system',


admin.site.register(Transaction, TransactionAdmin)
