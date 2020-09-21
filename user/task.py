from django.core.mail import send_mail

from yushu.celery import app
from celery import shared_task

from yushu.settings import EMAIL_HOST_USER


@shared_task
def sendemail(code,mail):
    subject='新注册用户激活'
    message = '亲爱的用户你好！欢迎注册xxx网站，当前正在进行用户激活，请点击链接激活：<a href="http://101.200.235.75:8000/user/active/?id={}">激活用户</a>' \
              '<br> 或者直接复制下面的地址访问：http://101.200.235.75:8000/user/active/?id={}'.format(code, code)
    send_mail(subject=subject,message=message,
              from_email=EMAIL_HOST_USER,recipient_list=[mail,],html_message=message)


@app.task
def changepassword(code,mail):
    subject='用户修改密码'
    message = '亲爱的用户你好！听说你忘了密码？当前正在进行用户密码修改，请确认此次为本人进行操作，请点击链接修改密码：<a href="http://101.200.235.75:8000/user/forget_password/?id={}">激活用户</a>' \
              '<br> 或者直接复制下面的地址访问：http://101.200.235.75:8000/user/forget_password/?id={}'.format(code, code)
    send_mail(subject=subject,message=message,
              from_email=EMAIL_HOST_USER,recipient_list=[mail,],html_message=message)

