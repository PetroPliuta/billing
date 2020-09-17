from rest_framework import serializers
from .models import Router


class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = ('id', 'ip_address', 'secret')
