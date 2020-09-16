from django.contrib import admin
from .models import MenuOption, Toppings, SubMenuOption, SizeDetail, SubMenuOptionDetail, ExtraToppings, Order, OrderDetail, OrderExtraTopping, OrderToppings,ExtraToppingsMeta
# Register your models here.
   
admin.site.register(MenuOption)   
admin.site.register(Toppings)
admin.site.register(SubMenuOption)
admin.site.register(SubMenuOptionDetail)
admin.site.register(SizeDetail)
admin.site.register(ExtraToppings)

admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(OrderToppings)
admin.site.register(OrderExtraTopping)
admin.site.register(ExtraToppingsMeta)

