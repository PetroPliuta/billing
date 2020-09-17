from django.contrib import admin
from .models import Router
from .forms import RouterForm


class RouterAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address')
    list_display_links = ('id', 'ip_address')
    search_fields = ('ip_address', )
    ordering = ("id",)
    form = RouterForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # if change:
        #     obj.disconnect()


admin.site.register(Router, RouterAdmin)
