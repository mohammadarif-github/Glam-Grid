from django.shortcuts import render,get_object_or_404
from . import models
from category.models import Category,MainCategory
from store.models import Product
from django.contrib.auth .decorators import login_required
from .forms import FilterForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

def shop(request):
    men_categories = Category.objects.filter(maincategory=1)
    women_categories = Category.objects.filter(maincategory=2)
    shoes_categories = Category.objects.filter(maincategory=3)
    return render(request,"Shop.html",{"men_categories":men_categories,"women_categories":women_categories,"shoe_catagories":shoes_categories})
    

def men(request,category_slug=None):
    maincategory = "Men"
    main_category_men = MainCategory.objects.get(name="Men")
    # Retrieve all categories associated with the MainCategory "Men"
    categories = Category.objects.filter(maincategory=main_category_men)
    
    if category_slug is None:
        products = []
        for category in categories:
            products_in_category = Product.objects.filter(category=category)
            products.extend(products_in_category)
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    
    return render(request, "Men.html", {"products":products, "categories": categories,"main":maincategory,})

def women(request, category_slug=None):
    maincategory = "Women"
    main_category_women = MainCategory.objects.get(name="Women")
    categories = Category.objects.filter(maincategory=main_category_women)
    
    if category_slug is None:
        products = []
        for category in categories:
            products_in_category = Product.objects.filter(category=category)
            products.extend(products_in_category)
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    
    return render(request, "Men.html", {"products": products, "categories": categories, "main": maincategory})

def shoes(request,category_slug=None):
    maincategory = "Shoe"
    main_category_men = MainCategory.objects.get(name="Shoes")
    categories = Category.objects.filter(maincategory=main_category_men)
    
    if category_slug is None:
        products = []
        for category in categories:
            products_in_category = Product.objects.filter(category=category)
            products.extend(products_in_category)
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    
    return render(request, "Shoes.html", {"products":products, "categories": categories,"main":maincategory,})



def description(request,product_id):
    product = models.Product.objects.get(id=product_id)
    return render(request,"description.html",{"product":product})


def filter_men(request):
    maincategory = "Men"
    main_category_men = MainCategory.objects.get(name="Men")
    categories = Category.objects.filter(maincategory=main_category_men)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    size = request.GET.get("size")

    products = Product.objects.filter(category__maincategory=main_category_men)

    if min_price:
        products = products.filter(price__gte=min_price) 
    if max_price:
        products = products.filter(price__lte=max_price) 
    if size:
        products = products.filter(sizes__name=size)

    return render(request, "Men.html", {"products": products, "categories": categories, "main": maincategory})
def filter_women(request):
    maincategory = "Women"
    main_category_women = MainCategory.objects.get(name="Women")
    categories = Category.objects.filter(maincategory=main_category_women)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    size = request.GET.get("size")

    products = Product.objects.filter(category__maincategory=main_category_women)

    if min_price:
        products = products.filter(price__gte=min_price) 
    if max_price:
        products = products.filter(price__lte=max_price) 
    if size:
        products = products.filter(sizes__name=size)

    return render(request, "Women.html", {"products": products, "categories": categories, "main": maincategory})

def filter_shoes(request):
    maincategory = "Shoes"
    main_category_shoes = MainCategory.objects.get(name="Shoes")
    categories = Category.objects.filter(maincategory=main_category_shoes)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    size = request.GET.get("size")

    products = Product.objects.filter(category__maincategory=main_category_shoes)

    if min_price:
        products = products.filter(price__gte=min_price) 
    if max_price:
        products = products.filter(price__lte=max_price) 
    if size:
        products = products.filter(sizes__name=size)

    return render(request, "Shoes.html", {"products": products, "categories": categories, "main": maincategory})
