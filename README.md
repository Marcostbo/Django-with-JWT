# JWT Authentication in Django Rest Framework

## How JWT works?

### Step 0: Set up Django

```console
python -m pip install Django
```
```
django-admin startproject djangojwt
```
```
python manage.py startapp djangojwtapp
```

### Step 1: Create models

```
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

### Step 2: Set up Django API REST

### Step 3: Set up JWT Authentication
