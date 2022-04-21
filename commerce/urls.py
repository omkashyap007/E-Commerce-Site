from django.urls import path 
from commerce import views as commerce_views

urlpatterns =[
    path("" , commerce_views.homePage , name = "site-home") ,
]