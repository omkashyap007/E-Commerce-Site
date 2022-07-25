from django.dispatch import receiver , Signal
from commerce.models import CartItem , Product
from django.db.models.signals import (
    post_save , 
    pre_save , 
    m2m_changed ,
    post_delete , 
    pre_delete 
)

@receiver(pre_save , sender = Product)
def changePriceOfAllProduct(sender , instance , **kwargs):
    all_cartitem_instance = instance.cartitem_set.all()
    for i in all_cartitem_instance :
        i.product.price = instance.price
        i.save()
    
# @receiver(pre_save , sender = CartItem)
def saveCartItem(sender , instance , **kwargs) :
    print("The cart Item has made some changes in it .. Hence they need to take affect here too !")
    instance.price = instance.product.price
    instance_total = instance.product.price*int(instance.quantity)
    if ( instance.product and instance.quantity ) and ( instance.total != instance_total ) :
        instance.total = instance_total
pre_save.connect(saveCartItem , sender = CartItem)


@receiver(post_save  , sender = CartItem)
def saveInititalPrice(sender , instance , created, *args , **kwargs):
    if created :
        print("The cart item was created in the database !")
        instance.price = instance.product.price
        instance.save()

# import os
# from django.conf import settings
# @receiver(pre_save  , sender = Product)
# def delete_previous_product_primary_image(sender , instance ,*args , **kwargs ):
#     if instance.id != None : 
#         if os.path.exists(os.path.join(BASE_DIR , "products/{}/primary_image/".format(instance.id))):
            
        
    
# @receiver(post_save , sender = Product)
# def save_new_product_primary_image(sender , instance , *args ,**kwargs):
