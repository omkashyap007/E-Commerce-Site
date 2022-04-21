from django.shortcuts import render , redirect

def homePage(request , *args , **kwargs) :    
    if request.user.is_authenticated : 
        if not request.user.is_verified :
            return redirect("unverified-email-useraccess") 
    context = {    
    }
    return render(request , "commerce/homePage.html" , context)