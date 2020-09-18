from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views

# Serializers define the API representation.
from .customer.views import CustomerViewSet
from .networking.views import RouterViewSet

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# # ViewSets define the view behavior.


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'routers', RouterViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    re_path(r'^api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    # # react
    path('', views.index),
    # path('customer/', include('billing.customer.urls')),
]

admin.site.site_header = "Billing Administration"
admin.site.site_title = "Billing Admin Portal"
admin.site.index_title = "Welcome to Billing Admin Portal"
