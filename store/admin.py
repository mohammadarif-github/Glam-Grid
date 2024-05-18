from django.contrib import admin
from . import models
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display = ('name',"category_name","price","is_available","in_stock","created")
    
    
    def category_name(self,obj):
        return obj.category.name
    
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Size)