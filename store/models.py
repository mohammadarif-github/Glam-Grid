from django.db import models
from category.models import Category
# Create your models here.


class Product (models.Model):
    name = models.CharField(max_length=50,unique=False)
    slug = models.SlugField(max_length=70,unique=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField(default="")
    image = models.ImageField(upload_to="images/products")
    price = models.IntegerField()
    price_before = models.IntegerField(blank=True,null=True,default=0)
    sizes = models.ManyToManyField("Size")
    in_stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    
class Size(models.Model):
    name = models.CharField(max_length=20,unique=True)
    
    def __str__(self):
        return self.name