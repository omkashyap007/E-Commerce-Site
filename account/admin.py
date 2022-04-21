from django.contrib import admin
from account.models import UserAccount
from django.contrib.auth.admin import UserAdmin

class UserAccountAdmin(UserAdmin) : 
	list_display = ["username" , "email" ,  "is_superuser"  ]
	
	search_fields = ["email" , "username"]
	readonly_fields = ["id" , "datejoined" , "lastlogin" , "is_verified" , "is_seller" , "seller_id" ]
	filter_horizontal = []
	list_filter = []
	fieldsets = []
	
admin.site.register(UserAccount , UserAccountAdmin)