from django.contrib import admin
from account.models import UserAccount , SellerAccount
from django.contrib.auth.admin import UserAdmin

class UserAccountAdmin(UserAdmin) : 
	list_display = ["username" , "email" ,  "is_superuser"  ]
	
	search_fields = ["email" , "username"]
	readonly_fields = ["id" , "datejoined" , "lastlogin" , "is_verified" , "is_seller" , "seller_id" ]
	filter_horizontal = []
	list_filter = []
	fieldsets = []
	
admin.site.register(UserAccount , UserAccountAdmin)

@admin.register(SellerAccount)
class SellerAccountAdmin(admin.ModelAdmin):
    list_display = ["user" , "seller_account_name" , "receiving_upi_id"]
    search_fields = ["user.username__startswith"]
    