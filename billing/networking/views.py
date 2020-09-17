from .models import Router
from rest_framework import viewsets
from .serializers import RouterSerializer
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend


class RouterViewSet(viewsets.ModelViewSet):
    queryset = Router.objects.all()
    serializer_class = RouterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('ip_address',)
