from django.db import models
from django.utils import timezone


class Customer(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True)
    mac_address = models.CharField(max_length=255, blank=True)
    added = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    online = models.BooleanField(default=False)
    last_online = models.DateTimeField(blank=True, null=True)
    # status = enabled, disabled
    description = models.TextField(blank=True, max_length=10**4)

    def __str__(self):
        return self.login

    def balance(self):
        transactions = Transaction.objects.filter(customer=self)
        sum = 0
        for transaction in transactions:
            sum = sum + transaction.amount
        return sum


class Transaction(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_time = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, max_length=10**4)

    def __str__(self):
        return str(self.id) + ' ' + str(self.date_time)

    class Meta:
        verbose_name = "Finance transaction"
        verbose_name_plural = "Finance transactions"
