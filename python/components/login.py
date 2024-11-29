import time, re,io
import json, xml.dom.minidom
import random

import logging

from pyqrcode import QRCode

from .. import config

logger = logging.getLogger('wxChat')

def load_login(core):
    core.login = login
    core.get_uuid = get_uuid
    core.get_QRcode = get_QRcode
    core.check_login = check_login


def login(self, enableCmdQR=False, picDir=None, qrCallback = None,loginCallback =None,exitCallback =None):
    # 判断是否已经登陆
    if self.isLogin or self.isLogging:
        logger.warning('已经登陆wxChat.')
        return
    self.isLogging= True
    while self.isLogging:
        logger.info("获取QRcode使用的uuid")
        while not self.get_uuid():
            time.sleep(1)
        logger.info('使用uuid下载 QR code.')
        qrStorage = self.get_QRcode(enableCmdQR=enableCmdQR,
            picDir=picDir, qrCallback=qrCallback)
        logger.info('请扫描QR code.')
        isLoggedIn = False
        while not isLoggedIn:
            status = self.check_login()
            if hasattr(qrCallback, '__call__'):
                qrCallback(uuid=self.uuid, status=status, qrcode=qrStorage.getvalue())
            if status == '200':
                isLoggedIn = True
            elif status == '201':
                if isLoggedIn is not None:
                    logger.info('Please press confirm on your phone.')
                    isLoggedIn = None
            elif status != '408':
                break
        if isLoggedIn:
            break
        elif self.isLogging:
            logger.info('Log in time out, reloading QR code.')
    else:
        return
    logger.info('Loading the contact, this may take a little while.')


def push_login(core):
    cookieDict = core.requests.cookies.get_dict()
    if 'uuid' in cookieDict:
        #  'https://login.weixin.qq.com/qrcode/YfClsW9kSw=='
        url= '%s/qrcode/%s' & (
            config.QR_LOGIN_URL,config.APP_ID
        )
    return False

def get_uuid(self):
    url = config.API_jsLogin
    params = {
        'appid' : config.APP_ID,
        'fun'   : 'new'
    }
    headers ={'User-Agent': config.USER_AGENT}
    response = self.requests.get(url,params=params,headers=headers)
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
    data = re.search(regx, response.text)
    if data and data.group(1) == '200':
        self.uuid = data.group(2)
        return  self.uuid
def get_QRcode(self, uuid=None, enableCmdQR=False, picDir=None, qrCallback=None):
    uuid = uuid or self.uuid
    picDir = picDir or config.QR_PATH
    qrStorage = io.BytesIO()
    response = self.requests.get('https://%s/qrcode/%s' % (config.LOGIN_HOST, uuid))
    
    if response.status_code == 200:
        qrStorage =  io.BytesIO(response.content)
        if hasattr(qrCallback, '__call__'):
            qrCallback(uuid=uuid, status='0', qrcode=qrStorage.getvalue())
        else:
            with open(picDir, 'wb') as f:
                f.write(qrStorage.getvalue())
        return qrStorage
    return
def check_login(self, uuid=None):
    uuid = uuid or self.uuid
    url = config.API_login
    localTime =int(time.time())
    params = 'loginicon=true&uuid=%s&tip=1&r=%s&_=%s' %(
        uuid, int(-localTime /1579),localTime
    )
    headers ={'User-Agent': config.USER_AGENT}
    response = self.requests.get(url,params=params,headers=headers)
    regx = r'window.code=(\d+)'
    data = re.search(regx, response.text)
    if data and data.group(1) == '200':
        if process_login_info(self, response.text):
            return '200'
        else:
            return '400'
    elif data:
        return data.group(1)
    else:
        return '400'

def process_login_info(core,loginContent):
    ''' when finish login (scanning qrcode)
     * syncUrl and fileUploadingUrl will be fetched
     * deviceid and msgid will be generated
     * skey, wxsid, wxuin, pass_ticket will be fetched
    '''
    regx = r'window.redirect_uri="(\S+)";'
    core.loginInfo['url'] = re.search(regx, loginContent).group(1)
    headers = { 'User-Agent' : config.USER_AGENT }
    response = core.requests.get(core.loginInfo['url'],headers=headers, allow_redirects = False)
    core.loginInfo['url'] = core.loginInfo['url'][:core.loginInfo['url'].rfind('/')]
    for indexUrl, detailedUrl in (
            ("wx2.qq.com"      , ("file.wx2.qq.com", "webpush.wx2.qq.com")),
            ("wx8.qq.com"      , ("file.wx8.qq.com", "webpush.wx8.qq.com")),
            ("qq.com"          , ("file.wx.qq.com", "webpush.wx.qq.com")),
            ("web2.wechat.com" , ("file.web2.wechat.com", "webpush.web2.wechat.com")),
            ("wechat.com"      , ("file.web.wechat.com", "webpush.web.wechat.com"))):
        fileUrl, syncUrl = ['https://%s/cgi-bin/mmwebwx-bin' % url for url in detailedUrl]
        if indexUrl in core.loginInfo['url']:
            core.loginInfo['fileUrl'], core.loginInfo['syncUrl'] = \
                fileUrl, syncUrl
            break
    else:
        core.loginInfo['fileUrl'] = core.loginInfo['syncUrl'] = core.loginInfo['url']
    core.loginInfo['deviceid'] = 'e' + repr(random.random())[2:17]
    core.loginInfo['logintime'] = int(time.time() * 1e3)
    core.loginInfo['BaseRequest'] = {}

    try:
        for node in xml.dom.minidom.parseString(response.text).documentElement.childNodes:
            if node.nodeName == 'skey':
                core.loginInfo['skey'] = core.loginInfo['BaseRequest']['Skey'] = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                core.loginInfo['wxsid'] = core.loginInfo['BaseRequest']['Sid'] = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                core.loginInfo['wxuin'] = core.loginInfo['BaseRequest']['Uin'] = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                core.loginInfo['pass_ticket'] = core.loginInfo['BaseRequest']['DeviceID'] = node.childNodes[0].data
    except Exception as e:
        logger.error('Your wechat account may be LIMITED to log in WEB wechat, error info:\n%s' % response.text)
        core.isLogging = False
        return False
    return True