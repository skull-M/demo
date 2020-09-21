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
    alipay_public_key_string = alipay_public_key_string,
    sign_type = 'RSA2',
    debug=False  # 默认False
)

# 如果你是 Python 3的用户，使用默认的字符串即可
subject = "鱼书购买鱼豆"

# 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="20200809213",
    total_amount=100,
    subject=subject,
    return_url=None,
    notify_url=None # 可选, 不填则使用默认notify url
)

alipay_url = 'https://openapi.alipaydev.com/gateway.do?'
url = alipay_url + order_string
print(url)