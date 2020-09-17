# Generated by Django 3.1 on 2020-09-17 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('networking', '0002_router_description'),
        ('customer', '0010_auto_20200917_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='last_online',
            new_name='last_online_datetime',
        ),
        migrations.AddField(
            model_name='customer',
            name='last_online_ip',
            field=models.GenericIPAddressField(blank=True, null=True, protocol='IPv4'),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_online_router',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='networking.router'),
        ),
    ]