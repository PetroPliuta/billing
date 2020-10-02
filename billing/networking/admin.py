from django.contrib import admin
from .models import Router
from .forms import RouterForm
from billing.customer.models import Customer
from billing.helpers import is_one_list_in_another_list


class RouterAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'ip_address'
    list_display_links = 'title', 'ip_address'
    search_fields = 'title', 'ip_address'
    ordering = 'id',
    form = RouterForm

    def save_model(self, request, obj, form, change):
        if change:
            old_router = self.model.objects.get(id=obj.id)
            customers = Customer.objects.filter(last_online_router=old_router)
        super().save_model(request, obj, form, change)
        Router.generate_config()
        Router.restart_radius()
        if change and is_one_list_in_another_list(('ip_address', 'secret'), form.changed_data):
            for customer in customers:
                customer.disconnect(old_router)

    def delete_model(self, request, obj):
        # TODO: disconnect customers
        super().delete_model(request, obj)
        Router.generate_config()
        Router.restart_radius()

    def delete_queryset(self, request, queryset):
        # TODO: disconnect customers
        queryset.delete()
        Router.generate_config()
        Router.restart_radius()


admin.site.register(Router, RouterAdmin)
