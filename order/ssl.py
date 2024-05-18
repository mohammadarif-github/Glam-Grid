import string
import random
from django.contrib.auth.decorators import login_required  
from .models import PaymentGateWaySettings
from sslcommerz_lib import SSLCOMMERZ

def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required(login_url="login")
def sslcommerz_payment_gateway(request,id,grand_total):
    
    gateway_auth_details = PaymentGateWaySettings.objects.all().first()
    
    settings = {'store_id': gateway_auth_details.store_id,
                'store_pass': gateway_auth_details.store_pass, 'issandbox': True}
    
    sslcommez = SSLCOMMERZ(settings)
    post_body = {
        'total_amount': grand_total,
        'currency': "BDT",
        'tran_id': unique_transaction_id_generator(),
        'success_url': 'http://127.0.0.1:8000/order/success/',
        'fail_url': 'http://127.0.0.1:8000/order/failed/',
        'cancel_url': 'http://127.0.0.1:8000/home',
        'emi_option': 0,
        'cus_email': request.user.email,  # Retrieve email from the current user session
        'cus_phone': "request.user.phone",  # Retrieve phone from the current user session
        'cus_add1': "request.user.address",  # Retrieve address from the current user session
        'cus_city': "request.user.city",  # Retrieve city from the current user session
        'cus_country': 'Bangladesh',
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,
        'product_name': "Test",
        'product_category': "Test Category",
        'product_profile': "general",

        # OPTIONAL PARAMETERS
        'value_a': id,
        'value_b': request.user.id
    }

    response = sslcommez.createSession(post_body)
    # print(response)
    # return JsonResponse(response)
    return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]