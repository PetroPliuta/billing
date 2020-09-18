from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'login', 'password', 'ip_address',
                  'mac_address', 'active', 'online', 'last_online_datetime',
                  'last_online_ip', 'last_online_router', 'balance', 'download_speed', 'upload_speed')
