#需要验证用户登录权限的
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

login_required = ['/user/personal/','/user/change_password/','/book/giftemail/','/book/seedrift/']

class LoginMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # print('path:',request.path)
        if request.path in login_required:
            if not request.user.is_authenticated:
                return render(request,'auth/login.html')