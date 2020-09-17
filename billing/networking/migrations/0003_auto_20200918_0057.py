# Generated by Django 3.1 on 2020-09-17 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networking', '0002_router_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='router',
            name='ip_address',
            field=models.GenericIPAddressField(protocol='IPv4', unique=True),
        ),
    ]
