import pickle

from celery import shared_task
from django.core.mail import send_mail

from yushu.celery import app
from yushu.settings import EMAIL_HOST_USER

#请求书
# @app.task(name='book.task.sendmail')
@app.task
# @shared_task
def sendmail(mail,message):
#     gift =pickle.loads(gift)
#     wish =pickle.loads(wish)
#     book =pickle.loads(book)
    subject = '鱼书【有人向你请求一本书】'
#     link = 'http://127.0.0.1:8000/book/senddrift/?g=' + str(gift.uidg.id)
#     message = '''
#     <p><stong>亲爱的 {},</stong></p>
# <p>{} 想要一本《{}》.你刚好有这本书在鱼书上等待赠送。</p>
# <p>点击<a
# href="{}">这里</a>查看书籍的邮寄地址.
# </p>
# <p>无论您是否愿意赠送{}这本书，都烦请您前往【鱼书】处理此请求。</p>
# <p>如果无法点击，你也可以将下面的地址复制到浏览器中打开:</p>
# <p>{}</p>
# <p>你的，鱼书</p>
# <p>
# <small>注意，请不要回复此邮件哦</small>
# </p>
# '''.format(gift.uidg.nickname, wish.uidw.nickname, book.bookname, link, wish.uidw.nickname, link)

    send_mail(subject=subject, message=message,
              from_email=EMAIL_HOST_USER, recipient_list=[mail,],
              html_message=message)

# 送别人书
# @app.task
# def sendemail_forsend(gift, user):
#     subject = '鱼书【有人赠送你一本书】'
#     link = 'http://127.0.0.1:8000/book/senddrift/?g=' + str(gift.id)
#     message = '''
#     <p><stong>亲爱的 {},</stong></p>
# <p>{}有一本《{}》可以赠送给你</p>
# <p>点击<a
#         href="{}">这里</a>填写书籍邮寄地址，
#     等待{}将书籍寄送给你
# </p>
# <p>如果无法点击，你也可以将下面的地址复制到浏览器中打开:</p>
# <p>{}</p>
# <p>你的，</p>
# <p>鱼书</p>
# <p>
#     <small>注意，请不要回复此邮件哦</small>
# </p>
#     '''.format(user.nickname, gift.user.nickname, gift.book.bookname, link, gift.user.nickname, link)
#     send_mail(subject=subject, message=message,
#               from_email=EMAIL_HOST_USER, recipient_list=[user.email ],
#               html_message=message)
@app.task
# @shared_task
def geinimail(mail,message):
#     gift =pickle.loads(gift)
#     wish =pickle.loads(wish)
#     book =pickle.loads(book)
    subject = '鱼书【有人向你赠送你想要的一本书】'
    send_mail(subject=subject, message=message,
              from_email=EMAIL_HOST_USER, recipient_list=[mail,],
              html_message=message)