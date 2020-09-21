import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from book.models import Book, Gift, Wish
from forms import UserForm
from user.models import User
from user.task import sendemail, changepassword
#分页定义
# def fenye(page,books):
#
#     per_page = 4
#     # 数据分页,recent
#     # 构造分页器
#     paginator = Paginator(books, per_page)
#     page_object = paginator.page(page)
#     book_list = page_object.object_list
#     print(book_list)
#     recent = list(book_list)
#     return recent
#个人主页
def index(request):
    # username = request.session.get('username')
    # print(username)
    books = Book.objects.all()
    # 分页器接收页码！！！！！！注意恶意传值
    page = int(request.GET.get('page', 1))
    per_page = 4
    # 数据分页,recent
    # 构造分页器
    paginator = Paginator(books, per_page)
    page_object = paginator.page(page)
    book_list = page_object.object_list
    print(book_list)
    recent = list(book_list)
    if (request.user.is_authenticated):
        # username = request.user.username
        # user = User.objects.filter(phone=username).first()
        user = request.user
        # print(user)
        # print(1111111111111111111111111111111)
        # print(books)

        return render(request,'index.html',locals())
    else:
        return render(request,'index.html',locals())


#注册页面
def register(request):
    if request.method == 'POST':
        #加载request.POST 里面的数据
        uform = UserForm(request.POST)
        if uform.is_valid():
            data = uform.cleaned_data
            #创建用户
            try:
                user = User.objects.create_user(
                    nickname=data['nickname'],
                    username=data['phone'],
                    password=data['password'],
                    email=data['email'],
                    phone=data['phone']

                )
                print(user)
                if user:
                    code = str(uuid.uuid4()).replace('-','')
                    #放到缓存中
                    cache.set(code,user)
                    #发送邮件

                    sendemail.delay(code,data['email'])
                    return HttpResponse('注册成功，请尽快进入邮箱激活使用')

            except Exception as err:

                print('user register---------------------------->',err)
                return render(request, 'auth/register.html')
        else:
            return render(request,'auth/register.html')
    else:
        return render(request, 'auth/register.html')

#注册时的手机验证
def checkphone(request):

    phone = request.GET.get('phone')
    phone1 = str(phone)
    a = phone1.isdigit()
    if not a:
        data = {
            "status": 400,
            'msg': '手机号格式错误，请重新输入'
        }
        return JsonResponse(data)
    else:
        user = User.objects.filter(phone=phone)

        if user:
            data = {
                "status":400,
                'msg':'手机号已存在，请重新输入'
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 200,
                'msg': '手机号可用'
            }
            return JsonResponse(data)

#注册时的邮箱验证
def checkemail(request):
    email = request.GET.get('email')
    print(email)
    import re
    a = re.match(r'[0-9a-zA-Z.]+@[0-9a-zA-Z.]+?com',email)

    print(a)
    if a:
        user = User.objects.filter(email=email).first()

        if user:
            data = {
                "status": 400,
                'msg': '邮箱已存在，请重新输入'
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 200,
                'msg': '邮箱可用'
            }
            return JsonResponse(data)
    else:
        data = {
            "status": 500,
            'msg': '邮箱未按照规则输入'
        }
        return JsonResponse(data)
#激活页面
def active(request):
    code = request.GET.get('id')
    user = cache.get(code)
    user1 = User.objects.filter(username=user.username).first()
    user1.is_active = True
    user1.save()
    # return HttpResponse('恭喜您激活成功！！！')
    return redirect('user:login')
#登录页面
def u_login(request):
    if request.method == 'GET':
        return render(request,'auth/login.html')

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        x = authenticate(username=username,password=password)
        if x:
            user = User.objects.filter(username=username).first()
            if user.is_active:
                # request.session['username'] = username
                login(request,user)
            # return render(request,'index.html',locals())
                return redirect(reverse('user:index'))
            else:
                return HttpResponse('用户还未激活，请去邮箱激活后登录')
        else:
            return HttpResponse('用户名密码错误')




#进入找回密码时的页面
def forget_password(request):
    if request.method == 'GET':
        code1 = request.GET.get('id')
        cache.set('code',code1)
        return render(request, 'auth/forget_password.html',locals())




#输入找回密码时的邮箱，发送邮件
def forget_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        import re
        a = re.match(r'[0-9a-zA-Z.]+@[0-9a-zA-Z.]+?com', email)
        if not a:
            return HttpResponse('输入邮箱格式有误，请重新返回输入')
        else:
            user = User.objects.filter(email=email)
            if not user:
                return HttpResponse('输入邮箱未注册')
            else:

                code = str(uuid.uuid4()).replace('-', '')
                # 放到缓存中
                cache.set(code, email)

                # 发送邮件

                changepassword.delay(code, email)

                return HttpResponse('请尽快去邮箱接收邮件进行密码修改')

    else:
        return render(request,'auth/forget_password_request.html')

#找回密码时获得code，联系邮箱，进行修改
def forget_password1(request):
    if request.method == 'POST':
        code = cache.get('code')
        print(code)
        print(type(code))
        email = cache.get(code)
        print(email)
        password = request.POST.get('password1')
        user = User.objects.filter(email=email).first()
        print(user)
        password = make_password(password)
        user.password = password
        user.save()
        # cache.delete('code')
        return render(request, 'auth/login.html')


def u_logout(request):
    logout(request)
    return redirect(reverse('user:index'))


def personal(request):
    user = request.user
    print(user)
    # cache.set('shuji',user)

    return render(request,'personal.html',locals())


def change_password(request):
    if request.method == 'GET':
        # id = request.GET.get('id')
        # user = User.objects.get(pk=id)
        # cache.set('useruser',user)
        return render(request,'auth/change_password.html')
    if request.method == 'POST':
        # user = cache.get('useruser')
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        if check_password(old_password,user.password):

            password = make_password(new_password)
            user.password = password
            user.save()
            login(request,user)
            # recent = Book.objects.filter(user_id_id=user.id)
            # return render(request,'index.html')
            return redirect(reverse('user:index'))
        else:
            return render(request,'auth/change_password.html',{'msg':'原密码输入错误'})


# def addbook(request):
#     if request.method == 'POST':
#         pass
#     return render(request,'auth/addbook.html')
def seebook(request):
    user = request.user
    bid = request.GET.get('bid')
    uid = request.GET.get('uid')
    book = Book.objects.get(pk=bid)

    #查看登录的这个人是否想赠送
    gift = Gift.objects.filter(bidg_id=bid).filter(uidg_id=user.id)

    # gifts = Gift.objects.filter(bidg_id=bid).filter(uidg_id=user.id)
    # 查看这本书是否有人想赠送
    gifts = Gift.objects.filter(bidg_id=bid)
    countg = gifts.count()

    # 查看登录的这个人是否想获取
    wish = Wish.objects.filter(bidw_id=bid).filter(uidw_id=user.id)

    # 查看这本书是否有人想获取
    wishes = Wish.objects.filter(bidw_id=bid)
    countw = wishes.count()
    if gift:
        has_in_gifts = True
    else:
        has_in_gifts = False
    if wish:
        has_in_wishes = True
    else:
        has_in_wishes = False

    return render(request,'book_detail.html',{'user':user,'book':book,'has_in_gifts':has_in_gifts,'has_in_wishes':has_in_wishes,'gifts':gifts,'wishes':wishes,'countg':countg,'countw':countw})