# Generated by Django 3.0.6 on 2020-06-01 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0005_auto_20200531_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='submenuoptiondetail',
            name='toppingsallowed',
            field=models.BooleanField(default=False),
        ),
    ]