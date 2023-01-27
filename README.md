# JWT Authentication in Django Rest Framework

This step-by-step guide seeks to present you an easy and reliable way to integrate JWT Authentication inside your Django application

Check Simple JWT documentation for more info: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/ 

## How JWT works?

## Step by step

### Step 0: Set up Django

```console
python -m pip install Django
```
```console
django-admin startproject djangojwt
```
```console
python manage.py startapp djangojwtapp
```

### Step 1: Create models

managers.py
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


models.py
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
admin.py
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
