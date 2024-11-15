from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
import uuid
# Create your models here.


class AppUserManager(BaseUserManager):
    def create_user(self,email, username, password=None):
            if not email:
                raise ValueError('An Email is Required')
            if not password:
                raise ValueError('A Password is Required')
            
            email = self.normalize_email(email)
            user = self.model(email=email,username=username)

            user.set_password(password)
            user.save()

            return user
    def create_superuser(self, email, username, password=None):
            if not email:
                raise ValueError('An email is required.')
            if not password:
                raise ValueError('A password is required.')
            
            user = self.create_user(email,username,password)

            user.is_superuser = True
            user.is_staff = True
            user.save()

            return user
    

class CustomUser(AbstractBaseUser,PermissionsMixin):
    
    email=models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=50)
    password=models.CharField(max_length=288)
    profilepic = models.ImageField(upload_to='profile_pictures', default='default.png')
    is_verified = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'profilepic']
    objects = AppUserManager()

    def __str__(self):
        return self.email

class UserThread(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True,blank=True)
    caption = models.TextField()
    image = models.ImageField(upload_to='posts', blank=True,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.title

class Comment(models.Model):
    user_thread = models.ForeignKey(UserThread, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"Comment by {self.author.username} on {self.user_thread.title} by {self.user_thread.author.username}"
    
class Members(models.Model):
     first_name = models.CharField(max_length=50)
     last_name = models.CharField(max_length=50)
     age = models.IntegerField()

     def __str__(self):
          return self.first_name
