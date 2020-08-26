from django.contrib import admin
from .models import Customer


def get_all_fields(class_):
    return [key for key in class_.__dict__.keys() if not key.startswith("__")]


class CustomerAdmin(admin.ModelAdmin):
    # list_display = list(get_all_fields(Customer))
    list_display = ('id', 'login', 'ip_address', 'online')
    list_display_links = ('login',)
    list_editable = ('ip_address',)
    list_filter = ('online',)
    readonly_fields = ('online',)
    save_as = True
    save_as_continue = False
    search_fields = ('login', 'ip_address', 'email')
    ordering = ("id",)


admin.site.register(Customer, CustomerAdmin)
