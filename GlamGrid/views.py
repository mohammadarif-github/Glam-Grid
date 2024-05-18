from django.shortcuts import render,redirect
from account.models import contact
from account.forms import ContactForm
from django.db.models import Q 
from store.models import Product

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about_us.html')


from django.contrib import messages

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the same page to clear the form
    return render(request,'Contact.html', {'form': form})


def search_product(request):
    searching_product = request.GET.get("search",'')
    print("SEArching term : " ,searching_product)
    products = Product.objects.filter(
        Q(name__icontains=searching_product) |                   
        Q(slug__icontains=searching_product) |                 
        Q(category__name__icontains=searching_product) |       
        Q(category__maincategory__name__icontains=searching_product) | 
        Q(price__icontains=searching_product)                 
    )
    return render(request, "search.html", {"products": products})
