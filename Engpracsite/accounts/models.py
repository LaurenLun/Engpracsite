from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.urls import reverse_lazy
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, usname, email, password=None):
        user = self.model(usname=usname, email=self.normalize_email(email))
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            usname = usname,
            email = email,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, usname, email, password=None):
        user = self.model(
            usname=usname,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    usname = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usname']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
    
    def get_absolute_url(self):
        return reverse_lazy('accounts:home')    
