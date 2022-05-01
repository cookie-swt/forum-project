from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    headportrait=models.ImageField()
    signature=models.CharField(max_length=50)
    pass

class Posting(models.Model):
    landlord_id=models.OneToOneField(User,on_delete=models.CASCADE)
    p_Title=models.CharField(max_length=20)
    p_Des=models.CharField(max_length=200)
    p_Date=models.DateField()
    p_See=models.BooleanField(default=True)

class Comment(models.Model):
    c_User_id=models.OneToOneField(User,on_delete=models.CASCADE)
    c_Content=models.CharField(max_length=500)
    c_Date=models.DateField()
    c_Likes=models.IntegerField(default=0)
    c_Posting_id=models.ForeignKey(Posting,on_delete=models.CASCADE)

class Collection(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    Posting_id=models.ForeignKey(Posting,on_delete=models.CASCADE)


