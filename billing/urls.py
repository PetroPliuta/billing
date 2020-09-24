from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from . import views

# Serializers define the API representation.
from .customer.views import CustomerViewSet
from .networking.views import RouterViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'routers', RouterViewSet)

urlpatterns = [
    re_path(r'^api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', views.index),
]

admin.site.site_header = "Billing Administration"
admin.site.site_title = "Billing Admin Portal"
admin.site.index_title = "Welcome to Billing Admin Portal"
