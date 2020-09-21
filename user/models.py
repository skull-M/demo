from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=30,null=False,blank=False)
    phone = models.CharField(max_length=11,unique=True,null=False,blank=False) #手机号
    email = models.EmailField(max_length=80,null=False,blank=False) #邮箱
    is_active = models.BooleanField(default=False) #是否激活
    beans = models.IntegerField(default=0) #鱼豆数量
    send_counter = models.IntegerField(default=0) #送出书的数量
    receive_counter = models.IntegerField(default=0) #收到书的数量

    class Meta:
        db_table = 'user'


    def __str__(self):
        return self.username










