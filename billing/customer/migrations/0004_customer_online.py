# Generated by Django 3.1 on 2020-08-18 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20200817_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
