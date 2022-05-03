from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.

def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}{1}.{2}'.format(instance.name, instance.identity_card, ext)
    return os.path.join(instance.major.name, filename) # 系统路径分隔符差异，增强代码重用性

class User(AbstractUser):
    headportrait=models.ImageField('头像',upload_to = user_directory_path, blank = True, null = True)
    signature=models.CharField(max_length=50)
    new_headportrait = ImageSpecField( # 注意：ImageSpecField 不会生成数据库表的字段
        source = 'headportrait',
        processors = [ResizeToFill(200, 200)],  # 处理成一寸照片的大小
        format = 'JPEG',  # 处理后的图片格式
        options = {'quality': 95}  # 处理后的图片质量
    )
    def photo_url(self):
        if self.new_headportrait and hasattr(self.new_headportrait, 'url'):
            return self.new_headportrait.url
        else:
            return '/media/default/user.jpg'

class Posting(models.Model):
    landlord_id=models.ForeignKey(User,on_delete=models.CASCADE)
    p_Title=models.CharField(max_length=20)
    p_Des=models.CharField(max_length=200)
    p_Date=models.DateField()
    p_See=models.BooleanField(default=True)

class Comment(models.Model):
    c_User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    c_Content=models.CharField(max_length=500)
    c_Date=models.DateField()
    c_Likes=models.IntegerField(default=0)
    c_Posting_id=models.ForeignKey(Posting,on_delete=models.CASCADE)

class Collection(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    Posting_id=models.ForeignKey(Posting,on_delete=models.CASCADE)


