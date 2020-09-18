from django.contrib import admin
from .models import Router
from .forms import RouterForm


class RouterAdmin(admin.ModelAdmin):
    list_display = ('ip_address', )
    list_display_links = ('ip_address', )
    search_fields = ('ip_address', )
    ordering = ("id",)
    form = RouterForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        Router.generate_config()
        Router.restart_radius()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        Router.generate_config()
        Router.restart_radius()

    def delete_queryset(self, request, queryset):
        queryset.delete()
        Router.generate_config()
        Router.restart_radius()


admin.site.register(Router, RouterAdmin)
