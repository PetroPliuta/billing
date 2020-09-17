from django.contrib import admin
from .models import Customer, Transaction
from .forms import CustomerForm


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'ip_address', 'balance', 'active', 'online')
    list_display_links = ('login',)
    list_editable = ('ip_address', 'active')
    list_filter = ('active', 'online')
    readonly_fields = ('online', 'balance', 'last_online_datetime',
                       'last_online_ip', 'last_online_router')
    save_as = True
    save_as_continue = False
    search_fields = ('login', 'ip_address', 'email')
    ordering = ("id",)
    form = CustomerForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            obj.disconnect()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        obj.disconnect()

    def delete_queryset(self, request, queryset):
        queryset.delete()
        for obj in queryset:
            obj.disconnect()


admin.site.register(Customer, CustomerAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'amount', 'date_time')
    list_display_links = ('customer', 'amount')
    list_filter = ('customer',)
    ordering = ("id",)


admin.site.register(Transaction, TransactionAdmin)
