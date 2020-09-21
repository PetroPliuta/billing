from django.db import models
from django.utils import timezone
from billing.networking.models import Router
from billing.tariff.models import InternetTariff
import subprocess


class Customer(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True)
    tariff = models.ForeignKey(
        to=InternetTariff, on_delete=models.SET_NULL, blank=True, null=True)
    ip_address = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True, unique=True)
    mac_address = models.CharField(
        max_length=255, blank=True, unique=True, null=True)
    active = models.BooleanField(default=True)
    online = models.BooleanField(default=False)
    last_online_datetime = models.DateTimeField(blank=True, null=True)
    last_online_ip = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True)
    last_online_router = models.ForeignKey(
        to=Router, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, max_length=10**4)
    added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.login

    def balance(self):
        transactions = Transaction.objects.filter(customer=self)
        sum = 0
        for transaction in transactions:
            sum = sum + transaction.amount
        return sum

    def download_speed(self):
        return self.tariff.download_speed_kbps if self.tariff else 0

    def upload_speed(self):
        return self.tariff.upload_speed_kbps if self.tariff else 0

    def disconnect(self):
        try:
            router = self.last_online_router
            if router:
                cmd = "echo 'User-Name={}' | /usr/bin/env radclient {}:3799 disconnect {} &"\
                    .format(self.login, router.ip_address, router.secret)
                subprocess.Popen(cmd, shell=True)
        except Exception as ex:
            print("radclient disconnect fail:", ex)

    def create_tariff_transaction(self):
        try:
            current_date = timezone.now().date()
            transactions = Transaction.objects.filter(
                customer=self, system=True, date_time__date=current_date)
            if len(transactions):
                raise Exception("Something wrong, system transaction for customer '{}' on date '{}' already present".format(
                    self.login, current_date))
            transaction = Transaction(
                customer=self, amount=-self.tariff.price, date_time=timezone.now(),
                comment="Monthly transaction for tariff plan '{}'".format(
                    self.tariff.title),
                system=True)
            transaction.save()
            if self.balance() < 0:
                self.disconnect()
        except Exception as ex:
            print("create_tariff_transaction error:", ex)


class Transaction(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, max_length=10**3)
    system = models.BooleanField("System transaction", default=False)

    def __str__(self):
        return str(self.id) + ' ' + str(self.date_time)

    class Meta:
        verbose_name = "Finance transaction"
        verbose_name_plural = "Finance transactions"
