from django.shortcuts import render , redirect
from commerce.models import Product , CartItem , Cart 
from django.http import HttpResponse
import json
from django.conf import settings
from django.contrib import messages
from account.models import UserAccount

def homePage(request , *args , **kwargs) :
    context = {
        "is_verified" : False, 
    }

    if request.user.is_authenticated : 
        user = request.user
        context["user"] = user
        context["cart_item_quantity"] = len(user.cart.products.all())
        if request.user.is_verified : 
            context["is_verified"] = True
        else :
            context["is_verified"] = False
    else : 
        context["user"] = None
    products = Product.objects.all()
    context["products"] = products
    return render(request , "commerce/homePage.html" , context)

def addItem(request  , *args , **kwargs) : 
    payload = {
        "user_verification" : "Unverified" ,
        "product_found" : "Product Not Found" , 
    }
    try : 
        if  request.user.is_authenticated : 
            user = request.user
        else : 
            user = None
    except : 
        user = None
    if not user :
        payload["user_verification"] = "Unverified"
    else : 
        payload["user_verification"] = "Verified"
    
    product_id = int(request.POST.get("product_id"))
    product_quantity = int(request.POST.get("product_quantity"))

    try : 
        product = Product.objects.get(id = product_id)
    except : 
        product = None
    
    if not product :
        payload["product_found"] = False
    else : 
        payload["product_found"] = True
        
    if not user or not product : 
        return HttpResponse(json.dumps(payload) , content_type = "application/json")
    
    if user.is_authenticated and product and user:
        payload["user_verfication"] = "Verified"
        
    # we have the user , the product and the quantity . now we need to add to the cart of the user.
    
    user_cart = user.cart
    cart_item = user_cart.checkProductInCart(product)
    if cart_item :
        print(cart_item)
        print("This item was in the cart !")
        cart_item.quantity += product_quantity 
        cart_item.total += (product_quantity*product.price)
    else : 
        print("This product was not in the cart !")
        product_total_price = product.price * product_quantity
        cart_item = CartItem(
            product = product, 
            quantity = product_quantity , 
            total = product_total_price , 
            itemcart = user_cart ,
        )
    cart_item.save()
    
    user_cart.products.add(cart_item)
    return HttpResponse(json.dumps(payload) , content_type = "application/json")
  

def saveItem(request , *args , **kwargs) :
    payload = {
        "user_verification" : "Unverififed" , 
        "product_found" : "Not found" , 
        "error": None ,
        "success" : False,
    }
    
    try : 
        if request.user.is_authenticated : 
            user = request.user
        else : 
            user = None
    except : 
        user = None
    if user : 
        payload["user_verification"] = "Verified"
    if not user : 
        payload["user_verification"] = "Unverified"
        
    product_id = int(request.POST.get("product_id"))
    try : 
        product = Product.objects.get(id = product_id)
    except Exception as e : 
        payload["error"] = str(e)
    
    if not request.user.is_authenticated or not product or not user : 
        return HttpResponse(json.dumps(paylaod) , content_tye = "appliaction/json")
    payload["success"] = True
    payload["error"] = None
    print(product)
    print(user)
    print("The user {} has saved it to its saved List".format(user.username))
    
    return HttpResponse(json.dumps(payload) , content_type = "application/json")    

def cartPage(request , *args , **kwargs) :
    if request.user.is_authenticated :
        user = request.user
    else :
        user = None
    if user :
        try : 
           cart = user.cart
        except :
            cart = None
    if not user :
        cart = None
        messages.error(request , "You are not verifed user and you cannot access the cart !")
        return render(request , "commerce/homePage.html")
    if not cart :
        messages.error(request , "You do not have a cart so you cannto access the cart !")
        return render(request , "commerce/homePage.html")
    
    cartItemsQuerySet = cart.products.all()
    cartItems = [
    ]
    for item in cartItemsQuerySet : 
        temp_dict = {}
        temp_dict["title"] = item.product.title
        temp_dict["image"] = item.product.product_primary_image
        temp_dict["quantity"] = item.quantity
        temp_dict["total_price"] = item.total
        temp_dict["price"] = item.product.price
        temp_dict["description"] = item.product.description[:100]
        temp_dict["cart_item_id"] = item.id
        temp_dict["proudct_id"] = item.product.id
        cartItems.append(temp_dict)
    context = {
        "cart_items" : cartItems , 
        "cart_item_quantity" : len(cartItems) ,
    }
    return render(request, "commerce/cartPage.html" , context)

def updateQuantity(request , *args , **kwargs) :
    payload = {
        "user_verification" : "User is not verfied !" ,
        "cart_verification" : "Cart is not found !" ,
        "product_verification" : "Product is not verified !" , 
        "user_cart_verification" : "The cart does not belong to the logged in user !" , 
        "response" : "The request was unsuccessfull" , 
        "product_update"  : "Product quantity was not updated !" , 
    }
    username = request.POST.get("user_username")
    try : 
        user = UserAccount.objects.get(username = request.POST.get("user_username"))
    except :
        user = None
    if not user : 
        payload["user_verification"] = "User is not verfied !"
        return HttpResponse(json.dumps(payload) , content_type = "application/json")
    payload["user_verification"] = "User is Verfied !"
    user_cart = user.cart
    if not user_cart :
        payload["cart_verifiction"] = "The logged in user don't have a cart !" 
        return HttpResponse(json.dumps , content_type = "application/json")
    cart_id = request.POST.get("cart_id") 
    try : 
        cart = Cart.objects.get(id = cart_id)
    except :
        cart = None
    if not cart :
        payload["user_cart_verification"] = "There is not cart with the id {} !".format(cart_id)
        return HttPResponse(json.dumps(payload) , content_type = "application/json")
    payload["cart_verification"] = "Cart is available !"
    if cart != user_cart:
        payload["user_cart_verification"] = "You are not allowed to change this cart items !"
        return HttpResponse(json.dumps(payload) , content_type = "application/json")
    payload["user_cart_verification"] = "The cart belongs to the current user !"
    update_quantity = request.POST.get("update_quantity")
    cart_product_id = request.POST.get("cart_product_id")
    try : 
        cartItemProduct = CartItem.objects.get(id = cart_product_id) 
    except : 
        cartItemProduct = None
    if not cartItemProduct :
        payload["product_verification"] = "There is not product with id {}".format(cart_product_id)
    payload["product_verification"] = "Found the product !"
        
    final_total_quantity = int(update_quantity)* float(cartItemProduct.product.price)
    cartItemProduct.total = final_total_quantity
    cartItemProduct.quantity = update_quantity
    cartItemProduct.save()
    
    payload["product_update"] = "The product quantity was successfully updated !"
    payload["response"] = "The request was successfull !"
    return HttpResponse(json.dumps(payload) , content_type = "application/json")
    

def serviceRecharge(request , *args , **kwargs) : 
    context = {}
    return render(request , "commerce/servicePage.html" , context)