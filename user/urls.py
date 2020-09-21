from django.urls import path

from user import views


app_name = 'user'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),

    path('checkphone/',views.checkphone,name='checkphone'),
    path('checkemail/',views.checkemail,name='checkemail'),
    path('active/',views.active,name='active'),
    path('login/',views.u_login,name='login'),
    path('logout/',views.u_logout,name='logout'),
    path('personal/',views.personal,name='personal'),
    path('change_password/',views.change_password,name='change_password'),

    path('forget_password/',views.forget_password,name='forget_password'),
    path('forget_password1/',views.forget_password1,name='forget_password1'),
    path('forget_password_request/',views.forget_password_request,name='forget_password_request'),
    # #添加书籍
    # path('addbook/',views.addbook,name='addbook')
    # #书籍详情
    path('seebook/',views.seebook,name='seebook')


]