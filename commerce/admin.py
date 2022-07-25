from django.contrib import admin
from commerce.models import Classification, Product, Cart , Order , CartItem
from django.utils.html import format_html


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ["id", "classification_type", "classification_description"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "seller_selling", "price", "discount"]

    @admin.display(description="Seller")
    def seller_selling(self, obj):
        seller_name = (
            str(obj.seller.user.firstname) + " " + str(obj.seller.user.lastname)
        )
        user_id = obj.seller.id
        url = "/admin/account/useraccount/{}/change/".format(user_id)
        html = """
            <a href = "{}">{}</a>
        """.format(
            url, seller_name
        )
        return format_html(html)
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["the_cart" , "cart_user"]
    
    def the_cart(self , obj) :
        return "{} : Cart".format(obj.owner.username)

    def cart_user(self , obj) :
        username = obj.owner.username
        user_id = obj.owner.id
        
        url = "/admin/account/useraccount/{}/change/".format(user_id)
        
        html_code_bit = """
            <a href= "{}">{}</a>
        """.format(url , username)
        return format_html(html_code_bit)
    the_cart.short_description = "The Cart"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin) : 
    list_display = ["the_order" , "the_buyer" , "total_price"]
    
    def the_order(self , obj) : 
        username = obj.buyer.username
        return "Order : {}".format(username)
    
    def the_buyer(self , obj) : 
        buyer_id = obj.buyer.id
        buyer_name = obj.buyer.username
        url = "/admin/account/useraccount/{}/change/".format(buyer_id)
        html_code_bit = """
        <a href = "{}">{}</a>
        """.format(url , buyer_name)
        return format_html(html_code_bit)
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin) :
    list_display = ["cart_item_data" , "item" , "product_quantity" , "price" ,"total_worth" , "the_cart"]
    
    @admin.display(description = "Item")
    def cart_item_data(self , instance):
        cart_user = instance.cart_set.all()[0].owner.username
        code_bit  = """{} 's Cart Item""".format(cart_user)
        return format_html(code_bit)
    
    @admin.display(description = "Item")
    def item(self , instance):
        product = instance.product
        product_title = product.title
        product_id = product.id
        url = "/admin/commerce/product/{}/change/".format(product_id)
        html_code_bit = """
            <a href = "{}">{}</a>
        """.format(url , product_title)
        return format_html(html_code_bit)

    @admin.display(description = "Quantity")
    def product_quantity(self , instance) : 
        return instance.quantity
        
    def price(self , instance):
        price = instance.product.price  
        return price
    price.short_description = "Price"
    
    @admin.display(description = "Total Price")
    def total_worth(self , instance):
        total_worth = instance.total
        return total_worth
    
    @admin.display(description = "Cart Link")
    def the_cart(self , instance):
        cart = instance.cart_set.all()[0]
        cart_id = cart.id

        url = "/admin/commerce/cart/{}/change/".format(cart_id)
        html_code_bit = """
            <a href = "{}">{}</a>
        """.format(url ,cart)
        return format_html(html_code_bit)