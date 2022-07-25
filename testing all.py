# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from django.db.models.signals import (
#     post_save
# )

# # here I am using django builtin model 
# # you can change it to whichever model you want 
# # and whatever model you are working with.

# @receiver(post_save , sender = User)
# def get_profile_image(sender , instance , created , *args , **kwargs) :
#     if created :
#         user = instance
#         user_id = instance.id
#         social_account = SocialAccount.objects.get(id = user_id)
        
#         extra_data = social_account.extra_data
#         extra_data = dict(extra_dict)
#         # if the extra_data gets converted to dict , then use this . 
#         #  else  : try using string splitting and all .
#         profile_pic = extra_data["picture"]
#         # this is a link
#         profile_pic = profile_pic
        
        
# url = "https://lh3.googleusercontent.com/ogw/ADea4I4tyj_B6alV9Ix79iDzwIdR-OYK6lgF5BbX008Cxw=s32-c-mo"


# import sys
# import requests
# from PIL import Image
# print("working")
# img = requests.get(url)
# print("done")
