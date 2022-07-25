from django.urls import path 
from commerce import views as commerce_views

urlpatterns =[
    # accessing services
    path("" , commerce_views.homePage , name = "site-home") ,
    path("site-service" , commerce_views.serviceRecharge , name = "site-service") ,
    path("add-item/" , commerce_views.addItem , name = "add-item")  , 
    path("save-item/" , commerce_views.saveItem , name = "save-item") ,
    path("cart/" , commerce_views.cartPage , name = "cart-item") ,
    
    # updating product data
    path("update-quantity/" , commerce_views.updateQuantity , name = "update-quantity") ,
]