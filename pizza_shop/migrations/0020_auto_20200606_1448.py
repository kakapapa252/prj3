# Generated by Django 3.0.6 on 2020-06-06 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0019_auto_20200606_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extratoppings',
            name='menu_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_shop.MenuOption'),
        ),
    ]