from django.db import models

# Create your models here.

class MainCategory(models.Model):
    name = models.CharField(max_length=50,unique=True)
    class Meta:
        verbose_name = "MainCategory"
        verbose_name_plural = "MainCategories"
        
    def __str__(self):
        return self.name
    

class Category(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=70, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional description field
    image = models.ImageField(upload_to="media/category", blank=True, null=True)  # Optional image field
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
