from django.shortcuts import render
from payment.models import Transaction
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

def rechargePayment(request , *args , **kwargs) :
    context = {}
    if request.method == "GET" : 
        return render(request , "payment/checkoutPayment.html" , context)
    if request.method == "POST" : 
        user = request.user
        amount = request.POST.get("amount")
        
        transaction = Transaction.objects.create(
            made_by = user ,
            amount = amount
        )
        transaction.save()
        print(transaction.amount)
        merchant_key = settings.PAYTM_SECRET_KEY
        params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/payment/recharge-callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = str(generate_checksum(paytm_params, merchant_key))

        transaction.checksum = str(checksum)

        paytm_params['CHECKSUMHASH'] = str(checksum)
        paytm_params["username"] = request.user.username
        print(paytm_params)
        print('SENT: ', checksum)
        return render(request, 'payment/redirect.html', context=paytm_params)

        
        

@csrf_exempt
def callbackPayment(request):
    if request.method == 'POST':
        print("This is the received data ")
        print(request.POST)
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            print("This is the user which is currently logged in ")
            print(request.user)
            print("")
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payment/callbackPayment.html', context=received_data)
        return render(request, 'payment/callbackPayment.html', context=received_data)
