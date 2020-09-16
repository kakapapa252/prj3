from django.urls import path, include
#from django.conf.urls import patterns, url
from django.http import HttpResponse
from pizza_shop import views
from django.conf.urls import url,include


urlpatterns = [
    path("", views.menu, name="menu"),
    path("checkout/", views.checkout, name="checkout"),
    path("loadcurrentcontext/", views.loadcurrentcontext , name="loadcurrentcontext"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("addToCart/", views.AddToCart.as_view(), name="addToCart"),
    path("completeorder/", views.completeorder, name="completeorder"),
    path("removeitem/", views.removeOrder, name="removeitem"),
    
]