import json
import os ,time ,requests
from datetime import datetime
from commerce.models import Cart 
from django.contrib import messages
from django.core.mail import send_mail
from account.models import UserAccount
from django.http import HttpResponse
from django.shortcuts import render , redirect 
from account.forms import UserRegisterForm , UserLoginForm
from django.contrib.auth import authenticate , login , logout
from account.scripts.getVariousMethods import getUUID , getErrorDict
from account.scripts.sendEmailActivation import sendActivationEmail , checkMailSent

        
"register-user"
def RegisterUser(request , *args , **kwargs) :
    if request.user.is_authenticated :
        messages.success(request , "You are already an authenticated user !") 
        return redirect("site-home")
    form = UserRegisterForm()
    errors = []
    if request.method == "POST" :
        form = UserRegisterForm(request.POST)
        if form.is_valid() : 
            user = form.save()
            auth_token = str(getUUID())
            user.auth_token = auth_token
            user.save()
            mail_sent = sendActivationEmail(user.email , user.auth_token , user.id )
            checkMailSent(mail_sent , request)
            login(request , user)
            return redirect("site-home")
        else : 
            errors = getErrorDict(form.errors)
    context = {
        "form" : form ,
        "errors" : errors 
    }
    return render(request , "account/authentication/registerUser.html" , context)

"login-user"
def LoginUser(request , *args , **kwargs) :
    if request.user.is_authenticated :
        messages.success(request , "You are already an authenticated user !")
        return redirect("site-home")
    
    form = UserLoginForm()
    errors = []
    if request.method == "POST" : 
        form = UserLoginForm(request.POST)
        if form.is_valid() : 
            user = form.save(request)
            return redirect("site-home") 
        else : 
            errors = getErrorDict(form.errors)
    context = {
        "form" : form ,
        "errors" : errors,
    }
    return render(request , "account/authentication/loginUser.html" , context)


"logout-user"
def LogoutUser(request , *args , **kwargs) : 
    if not request.user.is_authenticated : 
        messages.error(request , "You are already logged out !")
        return redirect("site-home")
    if request.user.is_authenticated : 
        logout(request)
    return redirect("site-home")


"verify-email-activation"
def VerifyEmailActivation(request , user_id , auth_token , *args , **kwargs) :
    if not request.user.is_authenticated : 
        messages.error(request , "You are not authenticated to receive email for verfication .Kindly login to get verification Email  !")
        return redirect("login-user")
    if request.user.is_verified : 
        messages.success(request,  "You are already verfied user !")
        return redirect("site-home")
    logged_in_user = request.user
    try : 
        user = UserAccount.objects.get(id = user_id)
    except Exception as e : 
        user = None
    if not user : 
        messages.error(request , "There is no such user with id = {}".format(user_id))
        return redirect("site-home")
    same_user = False
    user_auth_token = str(logged_in_user.auth_token)
    try : 
        auth_token = str(auth_token)
    except Exception as e : 
        auth_token = None
    if not auth_token : 
        messages.error(request , "There is no auth token to verify !")
        return redirect("site-home")
    if logged_in_user == user :
        same_user = True
        if auth_token == user_auth_token : 
            user.is_verified = True
            user.save()
            messages.success(request , "Your email account is verified . You can explore the Website now !")
            return redirect("site-home")
        else : 
            messages.error("The auth token is either expired or not valid !")
            return redirect("site-home")    
    else : 
        messages.error(request , "The Email activation link is not yours !")
        return redirect("site-home")
    messages.error(request , "No response")
    return redirect("site-home")

"send-email-verfication-link"
def sendEmailVerificationLink(request , *args , **kwargs) : 
    user = request.user
    if not user.is_authenticated : 
        messages.error("You cannot access this page !")
        return redirect("site-home")
    if user.is_verified:
        messages.success(request,  "You are already verified !")
        return redirect("site-home")
    if not user.is_verified:
        auth_token = str(getUUID())
        user.auth_token = auth_token
        user.save()
        email = user.email
        user_id = user.id
        mail_sent = sendActivationEmail(email , auth_token , user_id )
        checkMailSent(mail_sent ,request)
        return redirect("site-home")
    messages.error("No response !")
    return redirect("site-home")

def profilePage(request , *args  , **kwargs) :
    context = {
        "is_verified" : True, 
        "user" : None ,
    }
    if not request.user.is_authenticated : 
        return redirect("site-home")
    if not request.user.is_verified :
        context["is_verified"] = False
    user = request.user
    context["user"] = user 
    cart = Cart.objects.get(owner = user)
    print(cart.products.all())
    return render(request, "account/profilePage.html" , context)

def testingAjax(request, *args , **kwargs) :
    payload = {
        "data" : "Some data has to be sent , so this is the data !" ,  
        "response" :  "The request was successful." , 
    }
    return HttpResponse(json.dumps(payload) , content_type = "application/json")

# password for all
# OMpassword#123