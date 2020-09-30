from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from billing.networking.models import Router
from billing.tariff.models import InternetTariff
import subprocess
from random import randint


def rand_name():
    return "Customer #"+str(randint(1000, 9999))


class Customer(models.Model):
    full_name = models.CharField(
        max_length=255, default=rand_name)
    login = models.CharField(max_length=255, unique=True, default='user')
    password = models.CharField(max_length=255, blank=True, default='pass')
    tariff = models.ForeignKey(
        to=InternetTariff, on_delete=models.SET_NULL, blank=True, null=True)
    ip_address = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True, unique=True)
    active = models.BooleanField(default=True)
    online = models.BooleanField(default=False)
    last_online_datetime = models.DateTimeField(blank=True, null=True)
    last_online_ip = models.GenericIPAddressField(
        protocol='IPv4', blank=True, null=True)
    last_online_router = models.ForeignKey(
        to=Router, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, max_length=10**4)
    added = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return self.login

    def balance(self):
        s = sum(tr.amount for tr in self.transaction_set.all())
        return mark_safe(f"<span class='customer-balance{' balance-minus' if s<0 else ''}'>{s}</span>")
        # return s

    def download_speed(self):
        return self.tariff.download_speed_kbps if self.tariff else 0

    def upload_speed(self):
        return self.tariff.upload_speed_kbps if self.tariff else 0

    def disconnect(self, router=None):
        router_ = router or self.last_online_router
        try:
            if router_:
                stdin = f"echo 'User-Name=\'{self.login}\' {', Framed-IP-Address='+str(self.last_online_ip) if self.last_online_ip else ''}'"
                cmd = f"/usr/bin/env radclient {router_.ip_address}:3799 disconnect \'{router_.secret}\' &"
                subprocess.Popen(stdin+"|"+cmd, shell=True)
        except Exception as ex:
            print("radclient disconnect fail:", ex)

    def coa(self):
        try:
            if self.last_online_router:
                stdin = f"echo 'User-Name=\'{self.login}\', Mikrotik-Rate-Limit=\'{self.upload_speed()}k/{self.download_speed()}k\' \
                    {', Framed-IP-Address='+str(self.last_online_ip) if self.last_online_ip else ''}'"
                cmd = f"/usr/bin/env radclient {self.last_online_router.ip_address}:3799 coa \'{self.last_online_router.secret}\' &"
                subprocess.Popen(stdin+"|"+cmd, shell=True)
        except Exception as ex:
            print("radclient CoA fail:", ex)

    def create_tariff_transaction(self):
        """Creates monthly tariff transaction"""
        try:
            current_date = timezone.localtime().date()
            # print(timezone.localtime())
            transactions = self.transaction_set.filter(
                system=True, date_time__date=current_date)
            if transactions.count():
                raise Exception(
                    f"Something wrong, system transaction for customer '{self.login}' on date '{current_date}' already present")
            self.transaction_set.create(
                amount=-self.tariff.price, date_time=timezone.localtime(),
                comment=f"Monthly transaction for tariff plan '{self.tariff.title}'",
                system=True)
            if self.balance() < 0:
                self.disconnect()
        except Exception as ex:
            print("create_tariff_transaction error:", ex)


class Transaction(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_time = models.DateTimeField(default=timezone.localtime)
    comment = models.TextField(blank=True, max_length=10**3)
    system = models.BooleanField("System transaction", default=False)

    def __str__(self):
        return str(self.id) + ' ' + str(self.date_time)

    class Meta:
        verbose_name = "Finance transaction"
        verbose_name_plural = "Finance transactions"
