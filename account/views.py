from django.shortcuts import render,redirect
from .forms import RegistrationForm,UpdateForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#for sending mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from order.models import Order,Payment
from cart.models import Cart,CartItem
# Create your views here.

def registration(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirmation_link = f'http://127.0.0.1:8000/account/activate/{uid}/{token}'
            email_subject = "Confirmation Mail"
            email_body = render_to_string("confirm_mail.html",{"confirmation_link":confirmation_link})
            email = EmailMultiAlternatives(email_subject,"",to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            print("uid",uid)
            print ("token",token)
            return render(request,"check_mail.html")
            # login(request,user)
            # print(form.cleaned_data)
    return render(request,"register.html",{"form":form,})


def activate_user(request, uid, token):
    try: # Error handling kortechi. uid, user nao thakte pare tar mane sekhan theke error asar somvabona ache
    # sejonne code ke try er moddhe rakhlam
        print(token)
        uid_new = urlsafe_base64_decode(uid).decode() # encode kora sei uid ke decode kortechi
        target_user = User._default_manager.get(pk=uid_new) # decode er por je uid pelam seta kon 
        # user er seta janar jonne ei code ta
    except(User.DoesNotExist):
        target_user = None 
    if target_user is not None and default_token_generator.check_token(target_user, token):
        target_user.is_active = True
        target_user.save()
        return redirect('login')
    else:
        return redirect('register')


    
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=user_name, password=password)

        if user is not None:
            login(request,user)
            return redirect("homepage")
        else:
            messages.error(request,"Invalid username or password. Please try again.")
    return render(request,"login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    user = request.user
    return render(request,"profile.html",{"user":user})

def profile_update(request):
    user = request.user
    form = UpdateForm(instance=user)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request,'update.html',{'form':form})

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render (request,"order_history.html",{"orders":orders})

def order_details(request,id):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else None
    total_price = sum(item.sub_total() for item in cart_items) if cart_items else 0
    latest_order = Order.objects.get(id=id)
    return render(request,"order_details.html",{"order":latest_order,"cart_items":cart_items,"total_price":total_price})


def track_order(request,id):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else None
    total_price = sum(item.sub_total() for item in cart_items) if cart_items else 0
    order = Order.objects.get(id=id)
    progress_bar_status = {
        'Pending': order.status >= 1,
        'Accepted': order.status >= 2,
        'Placed': order.status >= 3,
        'Shipped': order.status >= 4,
        'Delivered': order.status >= 5
    }

    return render(request, "order_tracking.html", {
        "order": order,
        "cart_items": cart_items,
        "total_price": total_price,
        "progress_bar_status": progress_bar_status
    })
    
def transactions(request):
    user = request.user
    payments = Payment.objects.filter(user=user)
    return render (request,"transactions.html",{"payments":payments})

def recieved(request):
    orders = Order.objects.filter(status=5)
    return render (request,"recieved.html",{"orders":orders})


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import CustomPasswordChangeForm

# Custom PasswordChangeView
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'change_pass.html'
    success_url = reverse_lazy('password_change_done')

# Custom PasswordChangeDoneView
class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'pass_change_success.html'

# If you want to create custom views using function-based views
@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'password_change_form.html', {'form': form})

@login_required
def custom_password_change_done(request):
    return render(request, 'pass_change_success.html')