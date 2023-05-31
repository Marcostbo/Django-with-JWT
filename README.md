# JWT Authentication in Django Rest Framework

This step-by-step guide seeks to present you an easy and reliable way to integrate JWT Authentication inside your Django application

Check the Simple JWT documentation for more info: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/ 

## How JWT works?

When it comes to API authentication and server-to-server authorization, JSON web token (JWT) is particularly a useful technology. In terms of Single Sign-On (SSO), it means that a service provider can receive trustworthy information from the authentication server. 

By sharing a secret key with the Identity Provider, the Service Provider can hash a part of a token it receives and compare it to the signature of the token. Now, if that result matches the signature, the SP knows that the information provided has come from the other entity possessing the key.

The following workflow explains the authentication flow:

![image](https://user-images.githubusercontent.com/42622686/217071712-d89314b2-4cb6-48b3-b414-6a473aa7e1f9.png)

Usually the JWT follow this steps:

- User sign-in using username and password;
- The authentication server verifies the credentials and issues a JWT signed using a private key;
- Moving forward, the client will use the JWT to access protected resources by passing the JWT in the HTTP Authorization header;
- The resource server then verifies the authenticity of the token using the public key;
- The Identity Provider generates a JWT certifying user identity, and the resource server decodes and verifies the authenticity of the token using the public key.

Since the tokens are used for authorization and authentication in future requests and API calls great care must be taken to prevent security issues. These tokens shouldn’t be stored in publicly accessible areas like the browser’s local storage or cookies. In case there are no other choices, then the payload should be encrypted.

## Step by step

### Step 0: Set up Django

First, we need to install Django in our Python environment:

```console
python -m pip install Django
```
After that, create the new project and the new app:

```console
django-admin startproject djangojwt
```
```console
python manage.py startapp djangojwtapp
```

### Step 1: Create models

It is now possible to create and manipulate API models. The first model to be created is User, inheriting from AbstractUser, which is an abstract model provided by Django.

It is interesting to set the Username to null and use the email as the unique key, so the User model in models.py is built as follows:
```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from djangojwtapp.managers import CustomUserManager


class User(AbstractUser):
    username = None

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        app_label = 'djangojwtapp'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
```

We create a CustomUserManager inside managers.py (new file!) to handle all User creation:

```python
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

```
Finally, in the admin.py file, we register a new section in Admin to help us read and change all the users in User table
```python
from django.contrib import admin
from .models import User

admin.site.register(User)

```

### Step 2: Set up Django API REST

```console
python -m pip install djangorestframework
```

### Step 3: Set up JWT Authentication

```console
python -m pip install djangorestframework-simplejwt
```
Include the urls for JWT Authentication. The main path is the endpoint **/token/** to generate the access token.

```python
from django.urls import path
from .views import RegisterView, UserView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('logged-user/', UserView.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]
```
