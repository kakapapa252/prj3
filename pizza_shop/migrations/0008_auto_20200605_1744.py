# Generated by Django 3.0.6 on 2020-06-05 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0007_auto_20200605_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submenuoptiondetail',
            name='toppingsallowed',
        ),
        migrations.AddField(
            model_name='submenuoption',
            name='toppingsallowed',
            field=models.BooleanField(default=False),
        ),
    ]
