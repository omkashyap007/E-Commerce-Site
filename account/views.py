import os ,time ,requests
from datetime import datetime
from django.contrib import messages
from account.models import UserAccount
from django.core.mail import send_mail
from django.shortcuts import render , redirect 
from account.forms import UserRegisterForm , UserLoginForm
from django.contrib.auth import authenticate , login , logout
from account.scripts.sendEmailActivation import sendActivationEmail , checkMailSent
from account.scripts.getVariousMethods import getUUID , getErrorDict

        
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
    user = UserAccount.objects.get(id = user_id)
    user_auth_token = str(user.auth_token)
    auth_token = str(auth_token)
    if auth_token == user_auth_token : 
        user.is_verified = True
        user.save()
        messages.success(request , "Your email account is verified . You can explore the Website now !")
        return redirect("site-home")
    else : 
        messages.error(request , "The Email activation link is not yours !")
        return redirect("site-home")
    messages.error(request , "No response")
    return redirect("site-home")



"unverified-email-useraccess"
def unVerifiedEmailAccountAccess(request , *args , **kwargs) :
    user = request.user
    if not user.is_authenticated : 
        messages.error(request , "You have to login first to verify your email !")
        return redirect("login-user")
    if user.is_verified : 
        messages.success(request , "You are already verified user , Kindly explore the site !")
        return redirect("site-home")
    if not user.is_verified:
        user_id = user.id 
        auth_token = user.auth_token
    context = {
        "user" : user ,
        "user_id" : user_id ,
        "auth_token" : auth_token ,
    }
    return render(request , "account/authentication/unVerifiedAccountPage.html" , context )


"send-email-verfication-link"
def sendEmailVerificationLink(request , *args , **kwargs) : 
    user = request.user
    if user.is_verified:
        messages.success(request,  "You are already verified !")
        return redirect("site-home")
    if not user.is_verified:
        auth_token = user.auth_token
        user_id = user.id 
        email = user.email
        mail_sent = sendActivationEmail(email , auth_token , user_id )
        checkMailSent(mail_sent ,request)
        return redirect("site-home")
    return redirect("unverified-email-useraccess")




# nooneomme967@gmail.com
# thisPPaSS234&()