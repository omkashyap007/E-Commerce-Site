from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

def get_profile_image_file_path(self , filepath) : 
	return "profile_image/{}/profile_image.png".format(str(self.pk))

def get_default_profile_image():
	return "default_image.jpg"

class UserAccountManager(BaseUserManager):
    
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=email,
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password = None):
		user = self.create_user(
			email=email,
			username=username,
			password = password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_verified = True
		user.save(using=self._db)
		return user


class UserAccount(AbstractBaseUser):
	
	# user basic details 
	username = models.CharField(
		max_length=30,
		blank=False,
		null=False,
		unique=True
		)
	
	email = models.EmailField(
		verbose_name = "email",
		max_length=100,
		blank=False,
		null=False,
		unique=True
		)
	
	firstname = models.CharField(
		verbose_name = "FirstName",
		max_length=40,
		blank=True,
		null=True,
		)
	
	lastname = models.CharField(
		verbose_name = "LastName",
		max_length=40,
		blank=True,
		null=True
		)
	
	datejoined = models.DateTimeField(
		verbose_name="DateJoined", 
		auto_now_add=True,
	)
	lastlogin = models.DateTimeField(verbose_name="LastLogin", auto_now=True)
	
	profile_image = models.ImageField( 
		verbose_name = "Profile Image" ,
		upload_to = get_profile_image_file_path,
		default = get_default_profile_image ,
		blank = True , 
		null = True)
	
	
	# status details 
	is_verified = models.BooleanField(default = False)
	auth_token = models.CharField(max_length = 108 , blank = True , null = True)
	
	# seller details , seller_id = 0 [ if not seller ]
	is_seller = models.BooleanField(default = False)
	seller_id = models.IntegerField(verbose_name = "SellerId" , default = 0)
	
	# user auth credentials
	is_active = True
	is_admin = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	is_staff  = models.BooleanField(default = False)
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username" ]
	
	objects = UserAccountManager()

	def __str__(self) :
		if self.is_seller : 
			return "Seller -:> " + str(self.username) + " " + str(self.seller_id)
		return str(self.username)

	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	def has_perm(self, perm , obj = None) :
		return self.is_admin
	
	def has_module_perms(self, app_label):
		return True

		



class SellerAccount(AbstractBaseUser):
	...




class SellerAccountManager(BaseUserManager):
	...
	
	
# omkashyap002
# newPASSWORD123^&