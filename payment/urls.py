from django.urls import path
from payment import views as payment_views

urlpatterns = [
    path("recharge-payment/" , payment_views.rechargePayment, name = "recharge-payment"),
    path("recharge-callback/", payment_views.callbackPayment, name = "recharge-callback"),
]