from django.contrib import admin

# Register your models here.
from .models import Order,Payment,PaymentGateWaySettings


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(PaymentGateWaySettings)