from django.db import models
from django import forms


class Router(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    secret = models.CharField(max_length=32)
    description = models.TextField(max_length=10**3, blank=True)

    def __str__(self):
        return self.ip_address
