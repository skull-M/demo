from django.db import models

# Create your models here.
from user.models import User


class Book(models.Model):
    bookname = models.CharField(max_length=100,null=False,blank=False)
    author = models.CharField(max_length=100,null=False,blank=False)
    binding = models.BooleanField(choices=((0,'精装'),(1,'简装')))
    publisher = models.CharField(max_length=100, null=False, blank=False)
    pubdate = models.DateField(null=False,blank=False)
    price = models.FloatField(null=False,blank=False)
    pages = models.IntegerField(null=False,blank=False)
    isbn = models.CharField(max_length=30,null=False,blank=False)
    summary = models.CharField(max_length=255,null=False,blank=False)
    image = models.ImageField(upload_to='uploads/%Y/%m')
    date = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'book'
        ordering = ['-id']

    def __str__(self):
        return self.bookname

class Gift(models.Model):
    launched = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    bidg = models.ForeignKey(to=Book,on_delete=models.CASCADE)
    uidg = models.ForeignKey(to=User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'gift'
        ordering = ['-id']


class Wish(models.Model):
    launched = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    bidw = models.ForeignKey(to=Book,on_delete=models.CASCADE)
    uidw = models.ForeignKey(to=User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'wish'
        ordering = ['-id']

class Drift(models.Model):
    recipient_name = models.CharField(max_length=64,null=False,blank=False)
    address = models.CharField(max_length=256,null=False,blank=False)
    message = models.CharField(max_length=256,null=False,blank=False)
    mobile = models.CharField(max_length=16,null=False,blank=False)
    isbn = models.CharField(max_length=32,null=False,blank=False)
    book_title = models.CharField(max_length=64,null=False,blank=False)
    book_author = models.CharField(max_length=64,null=False,blank=False)
    book_img = models.ImageField(upload_to='driftbook/%Y/%m')
    requester_id = models.IntegerField(null=False,blank=False)
    requester_nickname = models.CharField(max_length=32,null=False,blank=False)
    gifter_id = models.IntegerField(null=False,blank=False)
    gift_id = models.IntegerField(null=False,blank=False)
    gifter_nickname = models.CharField(max_length=32,null=False,blank=False)
    status = models.IntegerField(default=0,null=False,blank=False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drift'
        ordering = ['-id']






