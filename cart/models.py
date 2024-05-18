from django.db import models
from store.models import Product, Size
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=70, blank=True)
    is_guest_cart = models.BooleanField(default=False)
    added_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.cart_id} - {'Guest' if self.is_guest_cart else self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name}  ; Size : ({self.size.name})"


