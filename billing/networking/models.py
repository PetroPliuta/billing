from django.db import models
from django import forms
from billing.settings import BASE_DIR
from random import randint


def rand_name():
    return "Router #"+str(randint(1000, 9999))


class Router(models.Model):
    title = models.CharField(max_length=255, blank=True, default=rand_name)
    ip_address = models.GenericIPAddressField(protocol='IPv4', unique=True)
    secret = models.CharField(max_length=32)
    description = models.TextField(max_length=10**3, blank=True)

    def __str__(self):
        return self.ip_address

    @staticmethod
    def generate_config():
        radius_clients_file = BASE_DIR/'config/radius_clients.conf'
        routers = Router.objects.all()
        with open(radius_clients_file, 'w') as f:
            for router in routers:
                router_config = f"""client {router.ip_address} {{
    ipaddr = {router.ip_address}
    secret = {router.secret}
    virtual_server = billing
}}
"""
                f.write(router_config)

    @staticmethod
    def restart_radius():
        try:
            import dbus
            sysbus = dbus.SystemBus()
            systemd1 = sysbus.get_object(
                'org.freedesktop.systemd1', '/org/freedesktop/systemd1')
            manager = dbus.Interface(
                systemd1, 'org.freedesktop.systemd1.Manager')
            manager.RestartUnit('freeradius.service', 'fail')
        except Exception as ex:
            print("Restart RADIUS error:", ex)
