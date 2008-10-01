from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as AuthGroup 


default_admin.register(User, UserAdmin)
default_admin.register(AuthGroup)
