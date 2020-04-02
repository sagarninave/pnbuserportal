from django.contrib import admin
from .models import User, UserFamily
from django.contrib.auth.models import Group

admin.site.register(User)
admin.site.register(UserFamily)
admin.site.unregister(Group)