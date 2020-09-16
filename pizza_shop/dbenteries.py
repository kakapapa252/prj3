import sqlite3
import csv
from sqlite3 import Error
from pizza_shop.models import MenuOption,SizeDetail,SubMenuOption,SubMenuOptionDetail,Toppings, ExtraToppings, ExtraToppingsMeta
from django.utils import timezone



db_file = r"C:\Users\15512\Projects\python\prj3\db.sqlite3"
conn = None
try:
    conn = sqlite3.connect(db_file)
except Error as e:
    print(e)

# Clearing out DB before entering records ===============
menuoptions = MenuOption.objects.all()
menuoptions.delete()
sizeObjects = SizeDetail.objects.all()
sizeObjects.delete()
toppingObjects = Toppings.objects.all()
toppingObjects.delete()
#================================================

f = open(r"C:\Users\15512\Projects\python\prj3\pizza_shop\Menu.csv")
reader = csv.reader(f)
currentMenuItems = ''
ctr = 0
size1 = None
size2 = None
size3 = None
menuitem = None


#print("Getting in loop")

for Menu, SubMenu, Small, Large, Regular, ContainExtra , NumberOfToppings, parentTopping, parentMenu in reader: 
    if(ctr == 0):
        ctr = ctr + 1
        size1 = SizeDetail(size_desc = Small) 
        # saving the size of the pizza in size table
        size1.save()
        size2 = SizeDetail(size_desc = Large) 
        # saving the size of the pizza in size table
        size2.save()
        size3 = SizeDetail(size_desc = Regular) 
        # saving the size of the pizza in size table
        size3.save()
    else:
        if (Menu.strip() != "" and Menu.strip() != "Toppings" and Menu.strip() != "Extra"): 
            #Saving the menu option in menu table
            displayExtraMenu = False
            if ContainExtra.strip() != '':
                displayExtraMenu = True
            date = timezone.localtime()
            menuitem = MenuOption(menu_desc = Menu.strip() , contains_extra = displayExtraMenu, create_date = date)
            currentMenuItems = Menu.strip()
            menuitem.save()
        elif Menu.strip() == "Toppings" or Menu.strip() == "Extra":
            currentMenuItems = Menu.strip()
        
        toppingsCount = 0
        toppingAllowed = True
        if NumberOfToppings.strip() != '':
            toppingsCount = int(NumberOfToppings)
        if toppingsCount == 0:
            toppingAllowed = False
        if (currentMenuItems != "Toppings" and currentMenuItems != "Extra"):
            submenuitem = SubMenuOption(menu_sub_desc = SubMenu, menu_option = menuitem, numberOfToppings = toppingsCount, toppingsAllowed = toppingAllowed)
            submenuitem.save()
            if(Small.strip() != ""):
                subdetail = SubMenuOptionDetail(price=Small,menusuboption=submenuitem,menusuboptionsize=size1)
                subdetail.save()
            if(Large.strip() != ""):
                subdetail = SubMenuOptionDetail(price=Large,menusuboption=submenuitem,menusuboptionsize=size2)
                subdetail.save()
            if(Regular.strip() != ""):
                subdetail = SubMenuOptionDetail(price=Regular,menusuboption=submenuitem,menusuboptionsize=size3)
                subdetail.save()
        elif (currentMenuItems == "Toppings"):
            toppings = Toppings(topping_desc=SubMenu)
            toppings.save()
        elif (currentMenuItems == "Extra"):
            topTopping = None 
            topMenu = None
            if(parentTopping.strip() != ''):
                topTopping = Toppings.objects.filter(topping_desc=parentTopping.strip()).get()
            if(parentMenu.strip() != ''):
                topMenu = MenuOption.objects.filter(menu_desc=parentMenu.strip()).get()
            extraToppingmeta = ExtraToppingsMeta(extratopping_desc=SubMenu,parent_topping=topTopping,menu_option=topMenu)
            extraToppingmeta.save()
            if(Small.strip() != ""):
                extraToppings = ExtraToppings(extratoppingmeta=extraToppingmeta,menusuboptionsize=size1,price=Small)
                extraToppings.save()
            if(Large.strip() != ""):
                extraToppings = ExtraToppings(extratoppingmeta=extraToppingmeta,menusuboptionsize=size2,price=Large)
                extraToppings.save()

