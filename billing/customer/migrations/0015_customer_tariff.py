# Generated by Django 3.1 on 2020-09-18 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tariff', '0001_initial'),
        ('customer', '0014_auto_20200918_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='tariff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tariff.internettariff'),
        ),
    ]