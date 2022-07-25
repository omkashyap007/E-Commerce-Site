from django.urls import path
from account import views as account_views

urlpatterns = [
    # authentications 
    path("authentication/register" , account_views.RegisterUser , name ="register-user"),
    path("authentication/login" , account_views.LoginUser , name ="login-user"),
    path("authentication/logout" , account_views.LogoutUser , name ="logout-user"),
    
    # email verifications
    path("authentication/verify-email/<int:user_id>/<str:auth_token>" , account_views.VerifyEmailActivation , name= "verify-email-activation"),
    path("authentication/send-email-verfication-link" , account_views.sendEmailVerificationLink , name = "send-email-verfication-link"),
    path("profile/" ,  account_views.profilePage , name = "profile-user"),
    
    path("ajax/testing/" , account_views.testingAjax , name = "check-for-ajax") ,
]