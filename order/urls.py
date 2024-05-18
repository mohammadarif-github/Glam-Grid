from django.shortcuts import redirect,render
from django.urls import path,include
from . import views
urlpatterns = [
    path("billing/",views.billing,name="billing"),
    path("success/",views.order_success,name="success"),
    path("order_summary/",views.order_summary,name="order_summary"),
    path("checkout/",views.checkout,name="checkout"),
    path("failed/",views.failed_view,name="failed"),
    
]
