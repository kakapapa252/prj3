# Generated by Django 3.0.6 on 2020-06-05 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0009_auto_20200605_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='toppings',
            name='menu_option',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pizza_shop.MenuOption'),
        ),
        migrations.AddField(
            model_name='toppings',
            name='price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='submenuoptiondetail',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
