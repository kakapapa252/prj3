# Generated by Django 3.0.6 on 2020-06-07 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0029_auto_20200607_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toppings',
            name='display',
        ),
        migrations.RemoveField(
            model_name='toppings',
            name='isextra',
        ),
    ]
