# from django.shortcuts import render


# def index(request):
#     return render(request, "customers/index.html")

from .models import Customer
from .serializers import CustomerSerializer
from rest_framework import viewsets


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
