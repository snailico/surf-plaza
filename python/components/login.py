import re,io
import logging

from pyqrcode import QRCode

from .. import config

logger = logging.getLogger('wxChat')

def load_login(core):
    core.login = login
    core.get_uuid = get_uuid
    core.get_QR = get_QR


def login(self, enableCmdQR=False, picDir=None, qrCallback = None,loginCallback =None,exitCallback =None):
    # 判断是否已经登陆
    if self.alive or self.isLogging:
        logger.warning('已经登陆wxChat.')
        return
    self.isLogging= True
    while self.isLogging:
        # 从cookie中获取uuid
        uuid = push_login(self)
        if uuid:
            qrStorage = io.BytesIO()
        else: 
            logger.info("获取QRcode使用的uuid")
            while not self.get_uuid():
                time.sleep(1)
            logger.info('使用uuid下载 QR code.')
            qrStorage = self.get_QR(enableCmdQR=enableCmdQR,
                picDir=picDir, qrCallback=qrCallback)
            logger.info('请扫描QR code.')
        self.isLogging = False



def push_login(core):
    cookieDict = core.requests.cookies.get_dict()
    if 'uuid' in cookieDict:
        #  'https://login.weixin.qq.com/qrcode/YfClsW9kSw=='
        url= '%s/qrcode/%s' & (
            config.QR_LOGIN_URL,config.APP_ID
        )
    return False

def get_uuid(self):
    url = '%s/jslogin' % config.LOGIN_HOST
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
def get_QR(self, uuid=None, enableCmdQR=False, picDir=None, qrCallback=None):
    uuid = uuid or self.uuid
    picDir = picDir or config.DEFAULT_QR
    qrStorage = io.BytesIO()
    response = self.requests.get('%s/qrcode/%s' % (config.QR_LOGIN_URL, uuid))
    
    if response.status_code == 200:
        qrStorage =  io.BytesIO(response.content)
        if hasattr(qrCallback, '__call__'):
            qrCallback(uuid=uuid, status='0', qrcode=qrStorage.getvalue())
        else:
            with open(picDir, 'wb') as f:
                f.write(qrStorage.getvalue())
        return qrStorage
    return
