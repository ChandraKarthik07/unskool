from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)
    bio=models.TextField(null=True)
    avatar=models.ImageField(null=True,default="avatar.svg")
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Room(models.Model):
    Host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    participants=models.ManyToManyField(User,related_name="participants")
    Topic=models.ForeignKey(Topic,on_delete=models.SET_NULL ,null=True)
    name=models.CharField(max_length=50)
    description=models.TextField(null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.name)

class Message (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,)
    room=models.ForeignKey(Room ,on_delete=models.CASCADE)
    body=models.TextField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.updated)


