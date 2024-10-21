import  logging

logger = logging.getLogger('wxChat')

def load_login(core):
    core.login = loginicon


def login(self,qrCallback = None,loginCallback =None,exitCallback =None):
    if self.alive or self.isLogging:
        logger.warning('wxChat has already logged in.')
        return
    self.isLogging= True
    while self.isLogging:
        uuid = push


def push_login(core):
    # cookieDict = core.s.cookies.get_dict()
    # if 'uuid' in cookieDict:
        #  'https://login.weixin.qq.com/qrcode/YfClsW9kSw=='
        url= '%s/qrcode/%s' & (
            config.QR_LOGIN_URL,config.APP_ID
        )
        