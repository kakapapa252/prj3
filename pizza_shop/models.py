#from django_mysql.models import JSONField
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django_mysql.models import

class MenuOption(models.Model):
    menu_desc = models.CharField(max_length=300)
    create_date = models.DateTimeField()
    contains_extra = models.BooleanField(default=False)

    def __str__(self):
        date = timezone.localtime(self.create_date)
        return f"'Menu Items {self.menu_desc}' created on {date.strftime('%A, %d %B, %Y at %X')}"

class SubMenuOption(models.Model):
    menu_option = models.ForeignKey(MenuOption, on_delete=models.CASCADE)
    menu_sub_desc = models.CharField(max_length=60)
    numberOfToppings = models.IntegerField(default=0)
    toppingsAllowed = models.BooleanField(default=False)

    def __str__(self):
        return f"''{self.menu_option}' Sub Menu '{self.menu_sub_desc}'  number of toppings {self.numberOfToppings} toppings allowed {self.toppingsAllowed}"

class SizeDetail(models.Model):
    size_desc = models.CharField(max_length=20)
    def __str__(self):
        return f" Size {self.size_desc}"


class SubMenuOptionDetail(models.Model):
    menusuboption = models.ForeignKey(SubMenuOption, on_delete=models.CASCADE)
    menusuboptionsize = models.ForeignKey(SizeDetail, on_delete=models.CASCADE)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f"submenu '{self.menusuboption}' for size '{self.menusuboptionsize}' Price '{self.price}'"


class Toppings(models.Model):
    topping_desc = models.CharField(max_length=60)

    def __str__(self):
        return f"topping '{self.topping_desc}''"

class ExtraToppingsMeta(models.Model):
    extratopping_desc = models.CharField(max_length=60)
    parent_topping = models.ForeignKey(Toppings, on_delete=models.CASCADE, blank=True, null=True)
    menu_option = models.ForeignKey(MenuOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"Extra Topping Desc '{self.extratopping_desc}' Parent Topping '{self.parent_topping}' Under Menu '{self.menu_option}'"


class ExtraToppings(models.Model):
    menusuboptionsize = models.ForeignKey(SizeDetail, on_delete=models.CASCADE, blank=True, null=True)
    extratoppingmeta = models.ForeignKey(ExtraToppingsMeta, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f"Extra topping Name '{self.extratoppingmeta}' size '{self.menusuboptionsize}' price '{self.price}'"

# Order placement tables
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    orderid = models.CharField(max_length=400, blank=False, null=False)
    orderplaced = models.BooleanField(default=False)
    date=models.DateTimeField(default=datetime.now(), blank=True)    

    def __str__(self):
        return f"Order id '{self.orderid}' User '{self.user}' date '{self.date}' Order Placed '{self.orderplaced}'"


class OrderDetail(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    submenuoptiondetail = models.ForeignKey(SubMenuOptionDetail, on_delete=models.DO_NOTHING)
    size = models.CharField(max_length=60,default='')
    submenuprice = models.FloatField(default=0.00)
    submenudesc = models.CharField(max_length=60)
    menudesc = models.CharField(max_length=60)

    def __str__(self):
        return f"'{self.orderid}'   '{self.submenuoptiondetail}'  '{self.size}'"



class OrderToppings(models.Model):
    orderdetail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    toppingid = models.ForeignKey(Toppings, on_delete=models.DO_NOTHING)
    toppingdesc = models.CharField(max_length=60)
    def __str__(self):
        return f"Order Detail '{self.orderdetail}' Topping  '{self.toppingid}' toppingdesc '{self.toppingdesc}'"



class OrderExtraTopping(models.Model):
    orderdetail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    extratoppingid = models.ForeignKey(ExtraToppings, on_delete=models.DO_NOTHING)
    extratoppingdesc = models.CharField(max_length=60)
    extratoppingprice = models.FloatField(default=0.00)
    def __str__(self):
        return f"Order Detail '{self.orderdetail}' Extra Topping id  '{self.extratoppingid}' extratoppingdesc '{self.extratoppingdesc}' extratoppingprice '{self.extratoppingprice}'"


class Testing(models.Model):
    test123 = models.ForeignKey(OrderExtraTopping, on_delete=models.CASCADE)
    abc = models.CharField(max_length=60)
    def __str__(self):
        return f"Order Detail '{self.test123}' Extra Topping id  '{self.abc}'"
