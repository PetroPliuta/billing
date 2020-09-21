from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from billing.customer.models import Customer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('period', choices=(
            'daily', 'hourly', 'minutely'), help='Cron period')

    def handle(self, *args, **options):
        try:
            getattr(self, options['period'])()
        except Exception as ex:
            self.stderr.write('Cron action fail:', ex)

    def daily(self):
        self.tariff_transactions()

    def hourly(self):
        self.disconnect_customers()

    def minutely(self):
        online_customers = Customer.objects.filter(online=True)
        for customer in online_customers:
            now = timezone.now()
            if (now-customer.last_online_datetime).total_seconds() > 120:
                self.stdout.write(
                    "'{}' - offline".format(customer.login))
                customer.online = False
                customer.save()

    def tariff_transactions(self):
        try:
            day_of_month = timezone.now().day
            if day_of_month != 1:
                return
            customers = Customer.objects.filter(tariff__isnull=False)
            for customer in customers:
                customer.create_tariff_transaction()
        except Exception as ex:
            self.stderr.write(ex)

    def disconnect_customers(self):
        try:
            customers = Customer.objects.all()
            for customer in customers:
                if customer.balance() < 0:
                    customer.disconnect()
        except Exception as ex:
            self.stderr.write(ex)
