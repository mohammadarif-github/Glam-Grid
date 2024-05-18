from django.urls import path,include
from . import views

urlpatterns = [
    path("view/",views.cart,name="cart"),
    path("add_to_cart/<int:product_id>/<int:size_id>/",views.add_to_cart,name="add_to_cart"),
    path("cart/remove_from_cart/<int:cart_item_id>/",views.remove_from_cart,name="remove_from_cart"),
    path("cart/decrease_item/<int:product_id>/",views.decrease_item,name="decrease"),
]
