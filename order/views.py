from django.shortcuts import render

# Create your views he
from django.shortcuts import render,redirect
from cart.models import Cart,CartItem
from .forms import BillingForm
from datetime import datetime
# from .ssl import sslcommerz_payment_gateway
from .models import Payment, Order
# from .ssl import sslcommerz_payment_gateway
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .ssl import sslcommerz_payment_gateway
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

def billing(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else None
    total_price = sum(item.sub_total() for item in cart_items) if cart_items else 0

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.order_total = total_price
            order.save()
            
            return redirect('order_summary')  # Redirect to a success page
    else:
        form = BillingForm()

    return render(request, 'billing.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})

@csrf_exempt
def order_success(request):
    if request.method == 'POST':
        data = request.POST

        # Retrieve user from POST data
        user_id = int(data['value_b'])
        user = get_object_or_404(User, pk=user_id)

        # Retrieve cart and cart items
        cart = Cart.objects.filter(user=user).first()
        cart_items = CartItem.objects.filter(cart=cart) if cart else None
        total_price = sum(item.sub_total() for item in cart_items) if cart_items else 0
        grand_total = total_price + 200

        # Create payment
        payment = Payment(
            user=user,
            payment_id=data['tran_id'],
            payment_method=data.get('card_issuer', 'N/A'),
            amount_paid=float(data['store_amount']),
            status=data['status']
        )
        payment.save()

        # Retrieve order details
        order_id = data['value_a']
        order_details = get_object_or_404(Order, id=order_id, user=user)
        
        # Attach payment to order
        order_details.payment = payment
        order_details.save()
        
        for item in cart_items:
            product = item.product
            product.in_stock -= item.quantity
            product.save()
            
        cart_items_data = list(cart_items)
        
        # Render the order complete page
        response = render(request, 'order_complete.html', {
            'order_details': order_details,
            'cart_items': cart_items_data,
            'total_price': total_price,
            'grand_total': grand_total,
            'payment_details': payment
        })
        
        # Delete cart and cart items after rendering the page
        cart_items.delete()
        cart.delete()

        return response
    else:
        return render(request, 'order_complete.html', {
            'error': 'Invalid request method'
        })

@login_required(login_url="login")
def order_summary(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else None
    total_price = sum(item.sub_total() for item in cart_items) if cart_items else 0
    latest_order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'order_summary.html', {'order': latest_order,"cart_items":cart_items,"total_price":total_price})

@login_required(login_url="login")
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else None
    total_price = sum(item.sub_total() for item in cart_items) if cart_items else 0
    order = Order.objects.filter(user=request.user).latest('created_at')
    grand_total= total_price+200;
    order_id = order.id
    return redirect(sslcommerz_payment_gateway(request,order_id,grand_total))

@csrf_exempt
def failed_view(request):
    return render(request,"failed.html")

