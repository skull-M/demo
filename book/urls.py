from django.urls import path, re_path
from django.views.static import serve

from book import views
from yushu import settings

app_name = 'book'

urlpatterns = [
    # path('')
    # 添加书籍
    path('gobook/', views.gobook, name='gobook'),
    path('addbook/', views.addbook, name='addbook'),
    path('sendbook/', views.sendbook, name='sendbook'),
    path('getbook/', views.getbook, name='getbook'),
    #赠送清单
    path('sendbooklist/', views.sendbooklist, name='sendbooklist'),
    #心愿清单
    path('getbooklist/', views.getbooklist, name='getbooklist'),
    path('delsendbook/', views.delsendbook, name='delsendbook'),
    path('delgetbook/', views.delgetbook, name='delgetbook'),
    path('mybooklist/', views.mybooklist, name='mybooklist'),
    path('findbook/', views.findbook, name='findbook'),
    path('giftemail/', views.giftemail, name='giftemail'),
    path('wishemail/', views.wishemail, name='wishemail'),
    #鱼漂页面，查看交易信息
    path('seedrift/', views.seedrift, name='seedrift'),
    #邮寄这本书
    path('yjbook/', views.yjbook, name='yjbook'),
    #拒绝送这本书
    path('jjbook/', views.jjbook, name='jjbook'),
    #撤销对这本书的请求
    path('cxbook/', views.cxbook, name='cxbook'),
    #支付页面
    path('pay/', views.pay, name='pay'),
    path('checkpay/', views.checkpay, name='checkpay'),

    # re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]