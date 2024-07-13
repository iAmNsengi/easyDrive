from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=User)
    avatar = models.ImageField(upload_to='driver/',null="True",default='avatar.jpg')
    category = models.CharField(max_length=100,null="True")
    bio = models.TextField(null="True")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.user.username + " " + self.category


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=User)
    avatar = models.ImageField(upload_to='company/',null="True",default='avatar.jpg')
    bio = models.TextField(null="True")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.user.username + " " + self.category


class Job(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    applicants = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.creator.username+" "+str(self.created_at)

