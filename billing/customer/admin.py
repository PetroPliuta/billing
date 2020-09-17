from django.contrib import admin
from .models import Customer, Transaction


# def get_all_fields(class_):
#     return [key for key in class_.__dict__.keys() if not key.startswith("__")]


class CustomerAdmin(admin.ModelAdmin):
    # list_display = list(get_all_fields(Customer))
    list_display = ('id', 'login', 'ip_address', 'balance', 'active', 'online')
    list_display_links = ('login',)
    list_editable = ('ip_address', 'active')
    list_filter = ('active', 'online')
    readonly_fields = ('online', 'balance')
    save_as = True
    save_as_continue = False
    search_fields = ('login', 'ip_address', 'email')
    ordering = ("id",)


admin.site.register(Customer, CustomerAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'amount', 'date_time')
    list_display_links = ('customer', 'amount')
    list_filter = ('customer',)
    ordering = ("id",)


admin.site.register(Transaction, TransactionAdmin)
