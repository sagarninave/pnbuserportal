from django.db import models
import uuid
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from pnb import settings
from django.contrib.auth.models import PermissionsMixin

GENDER = [
        ("male", 'male'),
        ("female", 'female'),
        ("other", 'other')
    ]

OCCUPATION = [
        ("business", 'business'),
        ("job", 'job')
    ]
      
ROLE = [
        ("admin", 'admin'),
        ("country head", 'country head'),
        ("state head", 'state head'),
        ("city head", 'city head'),
        ("constitucy head", 'constitucy head'),
        ("ward head", 'ward head'),
        ("branch head", 'branch head'),
        ("member", 'member')
    ]

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)

        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_Field):
      
        user = self.create_user(email,password=password, **extra_Field)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=10, unique=True, null=False, blank=False)
    aadhar = models.CharField(max_length=12, unique=True, null=False, blank=False)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    constitucy =  models.CharField(max_length=255, null=True, blank=True)
    ward =  models.CharField(max_length=255, null=True, blank=True)
    landmark =  models.CharField(max_length=255, null=True, blank=True)
    pincode =  models.IntegerField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20, default=None, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    role = models.CharField(choices=ROLE, max_length=20, null=True, blank=True)
    occupation_type = models.CharField(choices=OCCUPATION, max_length=20, null=True, blank=True)
    occupation_title = models.CharField(max_length=255, null=True, blank=True)
    otp = models.CharField(max_length=7, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)
    is_staff = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'aadhar']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "account_user"

    def __str__(self):
        return self.email + " - " + self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserFamily(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    age = models.IntegerField()
    occupation_type = models.CharField(choices=OCCUPATION, max_length=20, null=True, blank=True)
    occupation_title = models.CharField(max_length=255, null=True, blank=True)
    aadhar = models.CharField(max_length=12, unique=True, null=False, blank=False)
    user = models.ForeignKey(User, related_name="user_relation", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + " (" + self.user.first_name + " " + self.user.last_name + ")"   
