from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.IntegerField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)


class Order(models.Model):
    STATUS = (
        (1,'Pending'),
        (2,'Accepted'),
        (3,'Placed'),
        (4,'Shipped'),
        (5,'Delivered'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    order_total = models.FloatField(null=True,blank=True)
    status = models.IntegerField(choices=STATUS,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f"Order of : {self.user.first_name} {self.user.last_name}"
    
    
    

class PaymentGateWaySettings(models.Model):
    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null = True)