# Generated by Django 3.1 on 2020-09-17 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_auto_20200917_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='description',
        ),
        migrations.AddField(
            model_name='transaction',
            name='comment',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]