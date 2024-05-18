from django.urls import path
from . import views

urlpatterns = [
    path("",views.shop,name="shop"),
    path("men/",views.men,name="men"),
    path("women/",views.women,name="women"),
    path("shoes/",views.shoes,name="shoes"),
    path("men/<str:category_slug>",views.men,name="men_filter"),
    path("women/<str:category_slug>",views.women,name="women_filter"),
    path("shoes/<str:category_slug>",views.shoes,name="shoes_filter"),
    path("men/filter/", views.filter_men, name="filter_men"),
    path("women/filter/", views.filter_women, name="filter_women"),
    path("shoes/filter/", views.filter_shoes, name="filter_shoes"),
    path("description/<int:product_id>/",views.description,name="description"),
]