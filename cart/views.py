from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product,Size
from .models import Cart,CartItem
# Create your views here.

@login_required(login_url="login")
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()  # Retrieve the cart
    cart_items = None
    total_price = 0
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)  # Retrieve cart items associated with the cart
        total_price = sum(item.sub_total() for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})

from django.db import IntegrityError

from django.shortcuts import redirect  # Import redirect to redirect the user after adding to cart

@login_required(login_url="login")
def add_to_cart(request, product_id, size_id):
    try:
        product = Product.objects.get(id=product_id)
        size = get_object_or_404(Size, id=size_id)  # Retrieve the Size instance
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
        if not created:
            # If the cart item already exists, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
        else:
            # If the cart item is created for the first time, set the initial quantity to 1
            cart_item.quantity = 1
            cart_item.save()
    except Product.DoesNotExist:
        pass
    return redirect("cart")  # Redirect the user to the cart page after adding to cart

@login_required(login_url="login")
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect("cart")


@login_required(login_url="login")
def decrease_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, product=product)
    if cart_items.exists():
        cart_item = cart_items.first()  # Assuming you want to decrease the quantity of the first item found
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    # Redirect back to the cart page
    return redirect("cart")

