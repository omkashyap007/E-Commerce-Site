from django.db import models


# cla ss Product(models.Model) :
#     name = models.CharField(max_length = 255 , blank= False , null = False)
 
# class Cart(models.Model) :
#     # owner = models.OneToOneField(AUTH_USER_MODEL , on_delete = models.CASCADE) 
#     # products = models.ManyToManyField(Product , on_delete = models.CASCADE)
#     # checkout = models.BooleanField(default = False)
#     ...
    
# class Orders(models.Model):
#     buyer = models.ForeignKey(AUTH_USER_MODEL , on_delete = models.CASCADE)
#     order_products = models.ManyToManyField(Product)
#     total_price = models.DecimalField(max_digits = 10 , decimal_places = 2)
#     have_paid = models.BooleanField(default = False)