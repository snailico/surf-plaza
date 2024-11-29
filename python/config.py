

# app_id
APP_ID ="wx782c26e4c19acffb"

# api key credential
API_KEY = ""

QR_PATH = 'QR.png'

LANG ="zh_CN"
# 用户代理
USER_AGENT = "Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


# api url 

HOST ="wx2.qq.com"

LOGIN_HOST ="login.weixin.qq.com"
FILE_HOST = "file.wx2.qq.com"
PUSH_HOME = "webpush.wx2.qq.com"

#  根据HOST不同而不通 
# if HOST.index("wx2.qq.com") > -1:
#     LOGIN_HOST ="login.weixin.qq.com"
#     FILE_HOST = "file.wx2.qq.com"
#     PUSH_HOME = "webpush.wx2.qq.com"

# elif HOST.index("wx8.qq.com") > -1:
#     LOGIN_HOST = "login.wx8.qq.com"
#     FILE_HOST = "file.wx8.qq.com"
#     PUSH_HOME = "webpush.wx8.qq.com"
# elif HOST.index("qq.com") > -1:
#     LOGIN_HOST = "login.wx.qq.com"
#     FILE_HOST = "file.wx.qq.com"
#     PUSH_HOME = "webpush.wx.qq.com"

# elif HOST.index("web2.wechat.com") > -1:
#     LOGIN_HOST = "login.web2.wechat.com"
#     FILE_HOST = "file.web2.wechat.com"
#     PUSH_HOME = "webpush.web2.wechat.com"
# elif HOST.index("wechat.com") > -1:
#     LOGIN_HOST = "login.web.wechat.com"
#     FILE_HOST = "file.web.wechat.com"
#     PUSH_HOME = "webpush.web.wechat.com"
        

# 需要用到RES_PATH的静态变量请参考 写在接近页面底部的 RES_IMG_DEFAULT
API_jsLogin =  "https://" + LOGIN_HOST + "/jslogin"

#  https://login.wx2.qq.com/jslogin?appid=wx782c26e4c19acffb&fun=new&lang=zh_CN&redirect_uri=encodeURIComponent(https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?mod=desktop)),
API_login = 'https://' + LOGIN_HOST + '/cgi-bin/mmwebwx-bin/login'
