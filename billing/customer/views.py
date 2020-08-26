from .models import Customer
from rest_framework import viewsets
from .serializers import CustomerSerializer
from django.shortcuts import render


def index(request):
    return render(request, "customers/index.html")


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
