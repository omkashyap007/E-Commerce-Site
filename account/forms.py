from django import forms
from django.conf import settings
from account.models import UserAccount
from django.contrib.auth import authenticate, login


class UserRegisterForm(forms.Form):

    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "id": "id_username",
                "class": "register__form__fields",
                "placeholder": "Create a Username !",
            }
        ),
        required=True,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "id_email",
                "class": "register__form__fields",
                "placeholder": "Enter your Email !",
            }
        ),
        required=True,
    )

    password1 = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_password_one",
                "class": "register__form__fields",
                "placeholder": "Create a Strong Password !",
                "minlength": 6,
            }
        ),
        required=True,
    )

    password2 = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_password_two",
                "class": "register__form__fields",
                "placeholder": "Enter the Confirmation password !",
                "minlength": 6,
            }
        ),
        required=True,
    )

    class Meta:
        model = UserAccount
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_count = len(UserAccount.objects.filter(username=username))

        if user_count:
            raise forms.ValidationError(
                "User with username '{}' already exists !".format(username)
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_count = len(UserAccount.objects.filter(email=email))

        if email_count:
            raise forms.ValidationError(
                "User with email '{}' already exists !".format(email)
            )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if not password1:
            raise forms.ValidationError("The password field should not be empty !")

        if len(password1) < 6:
            raise forms.ValidationError("The password length must be greater than 6 !")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise forms.ValidationError("The Confirmation password is required !")

        if password2 and password1 != password2:
            raise forms.ValidationError("The two password fields do not match !")

        return password2

    def save(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        user = UserAccount(username=username, email=email)
        user.set_password(password1)
        user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "id": "id_email",
                "class": "login__form",
                "name": "email",
                "placeholder": "Your email for login !",
                "autofocus": True,
            }
        ),
        required=True,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "id_password",
                "class": "login__form",
                "name": "password",
                "placeholder": "Your password for login !",
            }
        ),
        required=True,
    )

    class Meta:
        fields = "__all__"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Kindly enter the email !")
        else:

            try:
                user = UserAccount.objects.get(email=email)

            except UserAccount.DoesNotExist:
                user = None

            if not user:
                raise forms.ValidationError(
                    "No user with '{}' this email !".format(email)
                )

            return email

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        if not password:
            raise forms.ValidationError("Password is required to login !")

        try:
            user = authenticate(email=email , password = password)
        except Exception as e:
            print(str(e))
            user = None
        if not user : 
            raise forms.ValidationError("Invalid Password !")
        return password

    def save(self, request):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = authenticate(email=email, password=password)

        except Exception as e:
            user = None

        if not user:
            return None
        if user:
            login(request, user)
            return user
