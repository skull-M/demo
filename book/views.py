import datetime
import math
import pickle
import time
import uuid

from alipay import AliPay
from django.template import loader

from book.task import sendmail, geinimail
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

from django.urls import reverse

from book.models import Book, Gift, Wish, Drift

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
from user.models import User
from yushu.settings import PUBLIC_KEY, PRIVATE_KEY


def addbook(request):
    if request.method == 'POST':
        # user = cache.get('shuji')
        # print(user)

        user = request.user

        bookname = request.POST.get('bookname')
        author = request.POST.get('author')
        binding = request.POST.get('binding')
        publisher = request.POST.get('publisher')
        pubdate = request.POST.get('pubdate')
        price = request.POST.get('price')
        pages = request.POST.get('pages')
        isbn = request.POST.get('isbn')
        summary = request.POST.get('summary')
        image = request.FILES.get('image')
        book = Book()
        book.bookname = bookname
        book.author = author
        book.binding = binding
        book.publisher = publisher
        book.pubdate = pubdate
        book.price = price
        book.pages = pages
        book.isbn = isbn
        book.summary = summary
        book.image = image
        book.user_id_id = user.id
        book.save()
        user = User.objects.filter(pk=user.id).first()
        user.beans += 1
        user.save()
        # recent = Book.objects.filter(user_id_id=user.id)
        recent = Book.objects.all()

        return render(request,'index.html',{'recent':recent,'user':user})




def gobook(request):
    # user = request.user
    return render(request,'auth/addbook.html',locals())

#赠送书籍返回时
def sendbook(request):
    bid = request.GET.get('bid')
    uid = request.GET.get('uid')
    user = request.user
    # print(bid)
    # print(uid)
    # book = Book.objects.get(pk=bid)
    # #查询数据库
    # gift = Gift.objects.filter(bidg_id=bid).filter(uidg_id=uid)
    # wish = Wish.objects.filter(bidw_id=bid).filter(uidw_id=uid)
    # #存在直接返回页面
    # if gift:
    #     has_in_gifts = True
    #     if wish:
    #         has_in_wishes = True
    #     else:
    #         has_in_wishes = False
    #     return render(request, 'book_detail.html',
    #                   {'user': user, 'book': book, 'has_in_gifts': has_in_gifts, 'has_in_wishes': has_in_wishes})
    #
    # #数据库中不存在则添加心愿清单
    # else:
    #     if wish:
    #         has_in_wishes = True
    #         has_in_gifts = False
    #         return render(request, 'book_detail.html',
    #                       {'user': user, 'book': book, 'has_in_gifts': has_in_gifts, 'has_in_wishes': has_in_wishes})
    #
    #     else:
    #         has_in_wishes = False
    gift = Gift()
    gift.uidg_id = user.id
    gift.bidg_id = bid
    gift.save()

    user = User.objects.filter(pk=user.id).first()
    user.beans += 1
    user.save()
    # has_in_gifts = True

    # return render(request, 'book_detail.html',
    #               {'user': user, 'book': book, 'has_in_gifts': has_in_gifts, 'has_in_wishes': has_in_wishes})
    return redirect(reverse('user:index'))
#尝试返回刷新失败！！
# def sendbook(request):
#     bid = request.GET.get('bid')
#     uid = request.GET.get('uid')
#     user = request.user
#     print(bid)
#     print(uid)
#     book = Book.objects.get(pk=bid)
#     gifta = Gift.objects.filter(bidg_id=bid).filter(uidg_id=uid)
#     wisha = Wish.objects.filter(bidw_id=bid).filter(uidw_id=uid)
#     if gifta:
#         has_in_gifts = True
#         return render(request, 'book_detail.html',
#                       {'user': user, 'book': book,  'has_in_gifts': has_in_gifts})
#     else:
#         gift = Gift()
#
#         gift.uidg_id = uid
#         gift.bidg_id = bid
#         gift.save()
#         has_in_gifts = False
#         return render(request, 'book_detail.html',
#                       {'user': user, 'book': book, 'has_in_gifts': has_in_gifts})


    # return render(request,'book_detail.html',{'book':book,'has_in_gifts':True})
    # return redirect(reverse('user:seebook'))
# def getbook(request):
#     bid = request.GET.get('bid')
#     uid = request.GET.get('uid')
#     user = request.user
#     print(bid)
#     print(uid)
#     book = Book.objects.get(pk=bid)
#     gifta = Gift.objects.filter(bidg_id=bid).filter(uidg_id=uid)
#     wisha = Wish.objects.filter(bidw_id=bid).filter(uidw_id=uid)
#     if wisha:
#         has_in_wishes = True
#         return render(request, 'book_detail.html',
#                       {'user': user, 'book': book,  'has_in_wishes': has_in_wishes})
#     else:
#         wish = Wish()
#
#         wish.uidw_id = uid
#         wish.bidw_id = bid
#         wish.save()
#         has_in_wishes = False
#         return render(request, 'book_detail.html',
#                       {'user': user, 'book': book, 'has_in_wishes': has_in_wishes})
#想要获得的书籍，点击时候的事件
def getbook(request):
    bid = request.GET.get('bid')
    uid = request.GET.get('uid')
    user = request.user
    # print(bid)
    # print(uid)
    # book = Book.objects.get(pk=bid)
    # #查询数据库，如果存在，就不添加
    # gift = Gift.objects.filter(bidg_id=bid).filter(uidg_id=uid)
    # wish = Wish.objects.filter(bidw_id=bid).filter(uidw_id=uid)
    #
    # if wish:
    #     if gift:
    #         has_in_gifts = True
    #     else:
    #         has_in_gifts = False
    #
    #     has_in_wishes = True
    #     return render(request, 'book_detail.html',
    #                   {'user': user, 'book': book, 'has_in_gifts': has_in_gifts, 'has_in_wishes': has_in_wishes})
    #
    # #加到数据库
    # else:
    #     if gift:
    #         has_in_gifts = True
    #         has_in_wishes = False
    #         return render(request, 'book_detail.html',
    #                       {'user': user, 'book': book, 'has_in_gifts': has_in_gifts, 'has_in_wishes': has_in_wishes})
    #
    #     else:
    #         has_in_gifts = False
    wish1 = Wish()
    wish1.uidw_id = user.id
    wish1.bidw_id = bid
    wish1.save()
    #判断是否存在然后渲染到前端
    return redirect(reverse('user:index'))

    # has_in_wishes = True
    # return render(request, 'book_detail.html',
    #               {'user': user, 'book': book, 'has_in_gifts': has_in_gifts, 'has_in_wishes': has_in_wishes})

#赠送清单 未实现多少人想要！！！
def sendbooklist(request):
    uid = request.user.id
    # page = int(request.GET.get('page', 1))
    user = request.user
    print(uid)
    gifts = Gift.objects.filter(uidg_id=uid)

    books = gifts
    page = int(request.GET.get('page', 1))
    # page = int(request.GET.get('page', 1))
    per_page = 3
    # 数据分页,recent
    # 构造分页器
    paginator = Paginator(books, per_page)
    #每页的数据
    page_object = paginator.page(page)
    book_list = page_object.object_list
    print(book_list)
    recent = list(book_list)

    return render(request,'my_gifts.html',locals())

#心愿清单
def getbooklist(request):
    uid = request.user.id
    print(uid)
    wishes = Wish.objects.filter(uidw_id=uid)

    page = int(request.GET.get('page', 1))
    # page = int(request.GET.get('page', 1))
    per_page = 3
    # 数据分页,recent
    # 构造分页器
    paginator = Paginator(wishes, per_page)
    # 每页的数据
    page_object = paginator.page(page)
    book_list = page_object.object_list
    print(book_list)
    recent = list(book_list)
    return render(request, 'my_wish.html',locals())


def delsendbook(request):

    bid = request.GET.get('bid')
    uid = request.GET.get('uid')

    sendgift = Gift.objects.filter(uidg_id=uid).filter(bidg_id=bid).first()
    Gift.delete(sendgift)

    return redirect(reverse('book:sendbooklist'))

def delgetbook(request):

    bid = request.GET.get('bid')
    uid = request.GET.get('uid')

    getwish = Wish.objects.filter(uidw_id=uid).filter(bidw_id=bid).first()
    Wish.delete(getwish)

    return redirect(reverse('book:getbooklist'))


def mybooklist(request):
    user = request.user
    books = Book.objects.filter(user_id_id=user.id)
    page = int(request.GET.get('page', 1))
    # page = int(request.GET.get('page', 1))
    per_page = 4
    # 数据分页,recent
    # 构造分页器
    paginator = Paginator(books, per_page)
    # 每页的数据
    page_object = paginator.page(page)
    book_list = page_object.object_list
    print(book_list)
    recent = list(book_list)
    return render(request,'gifts.html',locals())

#搜索框
def findbook(request):
    name = request.GET.get('q')
    books = Book.objects.filter(Q(bookname__contains=name)| Q(isbn__contains=name))
    return render(request,'search_result.html',{'books':books,'name':name})

#赠送
def giftemail(request):
    #进入填写地址
    if request.method == 'GET':


            #想要这本书的人
            user = request.user
            #这本书的id
            bid = request.GET.get('bid')
            #有这本书的人的id
            uid = request.GET.get('uid')

            # id = Book.objects.filter(pk=bid).first().user_id_id
            #赠送这本书的人的信息
            gifter = User.objects.filter(pk=uid).first()
            wisher = User.objects.filter(pk=user.id).first()
            if wisher.beans < 2:
                return render(request,'not_enough_beans.html',{'user':user})
            return render(request,'drift.html',locals())
        #判断是从邮箱进入

            #送的书的id
            #还需要判断登陆的人
            # user = request.user
            #
            # print(user)
            # bid = request.GET.get('bid')
            # #有此书的人的id
            # uid = request.GET.get('uid')
            # #1111111111111
            # id = Book.objects.filter(pk=bid).first().user_id_id
            #
            # gifter = User.objects.filter(pk=id).first()
            #
            # return render(request, 'drift.html', locals())
    #提交地址给拥有此书的人发邮件
    else:

        # @app.task
        # def woxiangyaoshu(subject, mail, message):
        #
        #     send_mail(subject=subject, message=message,
        #               from_email=EMAIL_HOST_USER, recipient_list=[mail, ], html_message=message)

        #想要这本书的人
        user = request.user
        #送的这本书的id
        bid = request.GET.get('bid')
        #赠送这本书的人的id
        uid = request.GET.get('uid')
        #赠送这本书的人的信息
        gifter = User.objects.filter(pk=uid).first()
        #想要这本书的人的信息
        wisher = User.objects.filter(pk=user.id).first()
        #赠送清单的这条信息
        gift = Gift.objects.filter(bidg_id=bid).filter(uidg_id=uid).first()
        #心愿清单的这条信息
        wish = Wish.objects.filter(bidw_id=bid).filter(uidw_id=user.id).first()
        #这本书的信息
        book = Book.objects.filter(pk=bid).first()

        #保存鱼漂信息
        drift = Drift()
        drift.recipient_name = request.POST.get('recipient_name')
        drift.address = request.POST.get('address')
        drift.message = request.POST.get('message')
        drift.mobile = request.POST.get('mobile')
        drift.isbn = book.isbn
        drift.book_title = book.bookname
        drift.book_author = book.author
        drift.book_img = book.image
        drift.requester_id = user.id
        drift.requester_nickname = wisher.nickname
        drift.gifter_id = gifter.id
        drift.gift_id = gift.id
        drift.gifter_nickname = gifter.nickname
        drift.save()

        # print(bid)
        # print(uid)


        #通知拥有此书 的人的邮箱
        mail = User.objects.filter(pk=uid).first().email
    #     print(mail)
    # #     cache.set()

        # subject = '鱼书'
        message = loader.render_to_string(
            'email/get_gift.html',
            {
                'gifter':gifter,
                'wisher':wisher,
                'book':book,
                'wish':wish
            }
        )
        sendmail.delay(mail,message=message)
        # # code = str(uuid.uuid4()).replace('-','')
        # cache.set(code,)
        # gift = pickle.dumps(gift1)
        # wish = pickle.dumps(wish1)
        # book = pickle.dumps(book1)
        # sendmail.delay(gift,wish,book)
    #


        return HttpResponse('已发送通知拥有本书的人，静待Ta去鱼书处理此请求请您耐心等待')

# uid是获取了想得到这本书的人的id
def wishemail(request):
    #有这本书的人
    user = request.user
    #赠送的书的id
    bid = request.GET.get('bid')
    #想要这本书的人的id
    uid = request.GET.get('uid')

    userid = user.id
    gifter = User.objects.filter(pk=user.id).first()
    wisher = User.objects.filter(pk=uid).first()

    book = Book.objects.filter(pk=bid).first()

    print(bid)
    print(uid)
    mail = User.objects.filter(pk=wisher.id).first().email
    print(mail)
    #邮件信息
    message = loader.render_to_string(
        'email/satisify_wish.html',
        {
            'gifter': gifter,
            'wisher': wisher,
            'book': book,
            'bid': bid,
            'uid':uid,
            'userid':userid
        }
    )
    #发送邮件
    geinimail.delay(mail,message=message)
    return HttpResponse('已发送通知想要本书的人，请您耐心等待后去鱼书处理')

#鱼漂页面
def seedrift(request):
    user = request.user
    drifts = Drift.objects.filter(Q(requester_id=user.id)|Q(gifter_id=user.id))
    userid = user.id
    return render(request,'pending.html',locals())

#点击邮寄
def yjbook(request):

    did = request.GET.get('did')
    drift = Drift.objects.filter(pk=did).first()
    wisher = User.objects.filter(pk=drift.requester_id).first()

    wisher.beans -= 2
    wisher.receive_counter += 1
    wisher.save()

    drift.status = 1
    drift.send_counter += 1
    drift.save()

    #请求成功点击邮寄后给两个鱼豆
    # request.user = User()
    # user = request.user
    # user.beans += 2
    # user.save()
    gifter = User.objects.filter(pk=drift.gifter_id).first()
    gifter.beans += 2
    gifter.save()
    return redirect('book:seedrift')

#拒绝请求者的请求
def jjbook(request):

    did = request.GET.get('did')
    drift = Drift.objects.filter(pk=did).first()
    drift.status = 3
    drift.save()
    return redirect('book:seedrift')

#作为请求者，撤回请求
def cxbook(request):

    did = request.GET.get('did')
    drift = Drift.objects.filter(pk=did).first()
    drift.status = 2
    drift.save()
    wisher = User.objects.filter(pk=drift.requester_id).first()
    wisher.beans += 2

    return redirect('book:seedrift')


def pay(request):
    money = request.GET.get('money')
    businessnumber = datetime.datetime.now() + money
    from alipay import AliPay

    from yushu.settings import PUBLIC_KEY
    from yushu.settings import PRIVATE_KEY

    alipay_public_key_string = open(PUBLIC_KEY).read()
    app_private_key_string = open(PRIVATE_KEY).read()

    alipay = AliPay(
        appid="2021000116697358",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2',
        debug=False  # 默认False
    )

    # 如果你是 Python 3的用户，使用默认的字符串即可
    subject = "鱼书购买鱼豆"

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        # out_trade_no="20200809213",
        out_trade_no=businessnumber,
        total_amount=money,
        subject=subject,
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    alipay_url = 'https://openapi.alipaydev.com/gateway.do?'
    url = alipay_url + order_string
    # print(url)
    return JsonResponse({'status':200,'url':url,'orderid':businessnumber})


def checkpay(request):
    orderid = request.POST.get('orderid')
    if not orderid:
        return JsonResponse({'status':500,'msg':'必须传递订单号'})
    alipay_public_key_string = open(PUBLIC_KEY).read()
    app_private_key_string = open(PRIVATE_KEY).read()

    alipay = AliPay(
        appid="2021000116697358",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2',
        debug=False  # 默认False
    )
    while True:
        response = alipay.api_alipay_trade_query(orderid)
        #判断response的结果
        print(response)
        if response.get('code')=='10000' and response.get('trade_status'):
            money = math.floor(response.get('total_amount'))
            request.user.beans += (money*2)
            request.user.save()
            return JsonResponse({'status':200,'msg':'支付成功！'})

        elif response.get('code' == '40004') or (
            response.get('code') == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
            time.sleep(3)
            continue
        else:
            print(response.get('code') )
            print(response.get('trade_status'))
            return JsonResponse({'status':500,'msg':'支付失败！'})
