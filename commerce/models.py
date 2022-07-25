from django.db import models
from account.models import UserAccount  , SellerAccount
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import UserAccount

def get_product_primary_image_path(self , filepath) :
    return "products/{}/primary_image/product_primary_image.png".format(self.pk)

def get_default_image_path() : 
    return "products/default_image.jpg"
    
# def get_product_secondary_image_path(self ,filepath) : 
#     return "products/{}/secondary_images/{}"
class Classification(models.Model):
    classification_type = models.CharField(max_length = 100 , blank = False , null = False)
    classification_description = models.TextField()  
    
    def __str__(self ) : 
        return str(self.classification_type) + " : " + str(self.classification_description)

class Product(models.Model) :
    title = models.CharField(max_length = 255 , blank= False , null = False)
    description = models.TextField(max_length = 1000 , blank = True , null = False)
    seller = models.ForeignKey(SellerAccount , on_delete = models.CASCADE)  
    product_primary_image = models.ImageField(
        default =  get_default_image_path , 
        upload_to = get_product_primary_image_path
    )
    price = models.DecimalField(max_digits = 15 , decimal_places = 2 , blank = False , null = False)
    discount = models.IntegerField(validators=  [MaxValueValidator(100) , MinValueValidator(0) ] , default = 0)
    product_type = models.ManyToManyField(Classification , blank = True , null = True)
    
    def __str__(self):
        return str(self.title) + " : " + str(self.seller.seller_account_name)
    
    
class Cart(models.Model) :
    owner = models.OneToOneField(UserAccount , on_delete = models.CASCADE) 
    products = models.ManyToManyField("commerce.CartItem" , blank = True , null = True)
    
    def __str__(self) : 
        return str(self.owner.username)+"'s Cart"
    
    def checkProductInCart(self , product) : 
        items = self.products.all()
        for item in items :
            if item.product == product :
                return item
        return False
		
class CartItem(models.Model) :
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits = 15 , decimal_places = 2 , blank= True  , null = True)
    price = models.DecimalField(max_digits = 15 , decimal_places = 2 , blank = False , null = False, default = 0)
    itemcart = models.ForeignKey("commerce.Cart" , on_delete = models.CASCADE , default = None)

    def __str__(self) : 
        return str(self.product.title) + " : " + str(self.total)
        
class Order(models.Model):
    buyer = models.ForeignKey(UserAccount , on_delete = models.CASCADE)
    order_products = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits = 10 , decimal_places = 2)
    have_paid = models.BooleanField(default = False)
    is_cash = models.BooleanField(default = False)
    is_online = models.BooleanField(default = False)
    
    def __str__(self) : 
        return str(self.buyer.username) +"'s order worth {} ₹".format(self.total_price)


# edrfasedDFED213!@#