from django.dispatch import Signal , receiver
from django.db.models.signals import (
    post_save , 
    pre_save , 
    post_delete , 
    pre_delete , 
    m2m_changed , 
)
from django.core.signals import (
    request_started , 
    request_finished 
)

from commerce.models import Cart , Product
from account.models import UserAccount

@receiver(post_save , sender = UserAccount)
def create_cart(sender , instance , created ,  *args , **kwargs):
    if created : 
        Cart.objects.create(owner = instance)
    
@receiver(post_save , sender = UserAccount)
def save_cart(sender , instance , *args , **kwargs) :
    instance.cart.save()
    
@receiver(pre_save , sender = Product)
def save_description(sender , instance , *args , **kwargs):
    if not instance.description : 
        instance.description = instance.title

# def checkUser(sender , environ , **kwargs):
    # if environ["PATH_INFO"] == "/" :
    #     for i in  environ:
    #         print(environ[i]
# request_started.connect(checkUser)

# pre_save signal is fired before an object is saved . so before saving the model object of product , if there is no description about the product , then assure that we fill description box with title.  

# we do not need to run instance.save() function because instance.save() will be run in  the post_save method or will be run directly . 

# @receiver(m2m_changed , sender = Cart.products.through)
# def user_cart_product_changed(sender , action , instance , model  , pk_set ,*args , **kwargs) :
#     if action == "post_remove":
#         print("Removed")


"""

"""