from django.contrib import admin
from .models import Router
from .forms import RouterForm
from billing.customer.models import Customer


class RouterAdmin(admin.ModelAdmin):
    list_display = ('ip_address', )
    list_display_links = ('ip_address', )
    search_fields = ('ip_address', )
    ordering = ("id",)
    form = RouterForm

    def save_model(self, request, obj, form, change):
        if change:
            customers = Customer.objects.filter(last_online_router=obj)
        super().save_model(request, obj, form, change)
        Router.generate_config()
        Router.restart_radius()
        if change:
            for customer in customers:
                customer.disconnect()

    def delete_model(self, request, obj):
        #TODO: disconnect customers
        super().delete_model(request, obj)
        Router.generate_config()
        Router.restart_radius()

    def delete_queryset(self, request, queryset):
        #TODO: disconnect customers
        queryset.delete()
        Router.generate_config()
        Router.restart_radius()


admin.site.register(Router, RouterAdmin)
