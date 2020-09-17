from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'login', 'password', 'ip_address',
                  'mac_address', 'active', 'online', 'last_online', 'balance',)
