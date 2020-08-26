from django.db import models


class Customer(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True)
    mac_address = models.CharField(max_length=255, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    online = models.BooleanField(default=False)
    # status = enabled, disabled

    def __str__(self):
        return self.login
