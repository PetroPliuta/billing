# Generated by Django 3.1 on 2020-09-18 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networking', '0003_auto_20200918_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='router',
            name='title',
            field=models.CharField(blank=True, default='Title', max_length=255),
        ),
    ]
