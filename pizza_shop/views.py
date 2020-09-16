import json
import uuid
import smtplib
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail as sm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from pizza_shop.models import MenuOption, SubMenuOptionDetail, Toppings, ExtraToppings, ExtraToppingsMeta, Order, OrderDetail, OrderExtraTopping, OrderToppings
from pizza_shop.forms import SignUpForm



def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session["userid"] = user.id
                request.session["username"] = user.first_name
                attachuseridwithorders(request)
        else:
            messages.add_message(request, messages.ERROR, "User Id Not Valid.")
    if request.session["currentpage"] == "menu":
        return HttpResponseRedirect(reverse("menu"))
    else:
        return HttpResponseRedirect(reverse("checkout"))

def signup(request):
    if request.method == 'POST':
        currentPage = request.session["currentpage"]
        currentuuid = request.session['uuid']
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            request.session["userid"] = user.id
            request.session["username"] = user.first_name
            request.session["currentpage"] = currentPage
            request.session['uuid'] = currentuuid
            attachuseridwithorders(request)
        else:
            for msg in form.error_messages:
                messages.add_message(request, messages.ERROR, msg)
    if request.session["currentpage"] == "menu":
        return HttpResponseRedirect(reverse("menu"))
    else:
        return HttpResponseRedirect(reverse("checkout"))

def attachuseridwithorders(request):
    try:
        if(request.session.get('uuid',None) is not None and request.session['uuid'] != ''):
            Order.objects.filter(orderid=request.session['uuid']).update(user=request.user)
    except Order.DoesNotExist:
        error = "Need to do error handling on this front."


def logout_user(request):
    logout(request)
    ret  = json.dumps({'success' : "1"})
    return HttpResponse(ret,content_type="application/json")


def menu(request):
    request.session["currentpage"] = "menu"
    if request.session.get('uuid', None) is None or request.session['uuid'] == '':
        request.session['uuid'] = str(uuid.uuid1())

    form = SignUpForm()
    userlogin = 0
    username = ''
    if request.session.get('userid', None) is None:
        userlogin = 0
    else:
        userlogin = 1
        username = request.session["username"]  
    tb_menuOptions = MenuOption.objects.prefetch_related("submenuoption_set__submenuoptiondetail_set__menusuboptionsize").all()
    tb_toppings = Toppings.objects.all()
    tb_extra_meta = ExtraToppingsMeta.objects.prefetch_related("extratoppings_set__menusuboptionsize").select_related("parent_topping","menu_option").all()
    return render(
        request,
        'pizza_shop/menu.html',
        {
            'menu_options': tb_menuOptions,
            'toppings' : tb_toppings,
            'extratopping' : tb_extra_meta,
            'userlogin' : userlogin,
            'username' : username,
            'form': form
        }
    )


class AddToCart(View):
    #@csrf_exempt exposing to external world csrf is used to run in internal network
    def post(self, request, *args, **kwargs):
        price = 0.0
        toppingsSelected = []
        extraItems = []
        requestJson = json.loads(request.POST["param"])
        if(len(requestJson["toppings"]) != 0):
            toppingsSelected = requestJson["toppings"].split(',')
        if(len(requestJson["extraitems"]) != 0):
            extraItems = requestJson["extraitems"].split(',')
        
        sid = SubMenuOptionDetail.objects.select_related('menusuboptionsize','menusuboption','menusuboption__menu_option').filter(id=requestJson["itemselected"]).get()#.select_related('menusuboption').select_related('menusuboption__menu_option').filter(id=requestJson["itemselected"]).get()
        menudetail = sid.menusuboption.menu_option
        sd = sid.menusuboption
        ss = sid.menusuboptionsize
        tops = Toppings.objects.filter(id__in=toppingsSelected).all()
        extraItems_tb = ExtraToppings.objects.filter(id__in=extraItems).select_related("extratoppingmeta").all()
        
        uuid = str(request.session["uuid"])
        orderRow = None
        try:
            orderRow = Order.objects.filter(orderid=uuid).get()
        except Order.DoesNotExist:
            orderRow = None

        if orderRow is None:
            user = None
            if request.user.id is not None :
                user = request.user
            orderRow = Order(user = user, orderid = request.session["uuid"])
            orderRow.save()

        od_tr = OrderDetail(orderid = orderRow, submenuoptiondetail = sid,size = ss.size_desc, submenuprice = sid.price, 
                submenudesc = sd.menu_sub_desc, menudesc = menudetail.menu_desc)
        od_tr.save()

        for top in tops:
            tp_tr = OrderToppings(orderdetail = od_tr, toppingid = top, toppingdesc = top.topping_desc)
            tp_tr.save()

        for extraItems_tr in extraItems_tb:
            toppingDetail = extraItems_tr.extratoppingmeta
            extp_tr = OrderExtraTopping(orderdetail = od_tr, extratoppingid = extraItems_tr, 
                                extratoppingdesc = toppingDetail.extratopping_desc, 
                                extratoppingprice = extraItems_tr.price)
            extp_tr.save()
        orderList = getCurrentOrders(request)    
        price = getTotalPrice(orderList)
        sessJson  = json.dumps({'price' : format(price, '.2f')})#, 'orders' : orderList.toJSON()})
        request.session['order'] = sessJson            
        return HttpResponse(sessJson,content_type="application/json")


def loadcurrentcontext(request):
    orderList = getCurrentOrders(request)    
    price = 0.0
    request.session["currentpage"] = "menu"
    if orderList is not None :
        price = getTotalPrice(orderList)
    return HttpResponse(json.dumps({'price' : format(price, '.2f')}),content_type="application/json")

def getCurrentOrders(request):
    fetchedOrder = Order.objects.prefetch_related("orderdetail_set__ordertoppings_set","orderdetail_set__orderextratopping_set").filter(orderid=str(request.session["uuid"])).all()
    return fetchedOrder

def getTotalPrice(orderList):
    totalPrice = 0.0
    for order in orderList:
        orderDetail = ''
        orderDetail = order.orderdetail_set.annotate(exPrice=Sum(f'orderextratopping__extratoppingprice')).all()  
        for orderDetailrow in orderDetail:
            if orderDetailrow.exPrice is None:
                totalPrice =  totalPrice + orderDetailrow.submenuprice
            else:
                totalPrice =  totalPrice + orderDetailrow.submenuprice + orderDetailrow.exPrice 
    return totalPrice

def checkout(request):
    orderList = getCurrentOrders(request)
    form = SignUpForm()
    request.session["currentpage"] = "checkout"
    price = 0.00
    if orderList is None :
        return HttpResponseRedirect(reverse("menu"))
    else:
        price = getTotalPrice(orderList)

        if(price == 0.0):
            return HttpResponseRedirect(reverse("menu"))
            
        if request.session.get('userid', None) == None:
            username = ''
        else:
            username = request.session["username"]
        return render(
            request,
            'pizza_shop/checkout.html',
            {
                'orderlist': orderList,
                'username' : username,
                'form': form,
                'price': price
            }
        )


def removeOrder(request):
    param = request.POST["param"]
    requestJson = json.loads(request.POST["param"])
    orderIdToRemove = requestJson["removeorderId"]
    orderdetail = OrderDetail.objects.filter(id=orderIdToRemove).get()
    orderdetail.delete()
    orderList = getCurrentOrders(request)
    price = 0.0
    if orderList is not None :
        price = getTotalPrice(orderList)
    ret = ''
    if (price > 0):
        ret = json.dumps({'success' : "1"})
    else:
        ret = json.dumps({'success' : "0"})
    return  HttpResponse(ret,content_type="application/json")

def render_template(template_filename, context):
    with open(template_filename) as file_:
        template = Template(file_.read())
    return template.render(context)


def completeorder(request):
    order = Order.objects.filter(orderid=request.session['uuid']).get()
    updateResult = Order.objects.filter(orderid=request.session['uuid']).update(orderplaced=True)
    orderList = getCurrentOrders(request)
    price = 0.00
    price = getTotalPrice(orderList)
    genId = request.session["uuid"]
    context ={
        'orderlist': orderList,
        'price': price,
        'orderid' : genId
    }
    email = order.user.email
    output = render_template("C:/Users/15512/Projects/python/prj3/pizza_shop/emailtemplate.txt", context)
    me = 'pizzeriatoyou@gmail.com'
    you = email
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('pizzeriatoyou@gmail.com','jupiter@12')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = me
        msg['To'] = you
        text = f'Your order places successfully. Your order id {genId}'
        html = output
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        smtp.sendmail(me,you,msg.as_string())
    ret = json.dumps({'success' : "1"})
    request.session['uuid'] = str(uuid.uuid1())
    messages.add_message(request, messages.INFO, f"Order placed successfully. Order id : {genId}. Mail sent at {email}")
    return HttpResponse(ret,content_type="application/json")


