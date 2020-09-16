# Generated by Django 3.0.6 on 2020-06-06 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_shop', '0014_submenuoption_toppingsallowed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraToppings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_topping_dec', models.CharField(max_length=60)),
                ('price', models.FloatField(default=0.0)),
                ('menusuboptionsize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_shop.SizeDetail')),
                ('toping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_shop.Toppings')),
            ],
        ),
    ]
