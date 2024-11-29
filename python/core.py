import requests

from .components import load_components

class Core(object):
    def __init__(self):
        self.isLogin, self.isLogging = False, False
        self.requests = requests.Session()
        self.uuid = None
        self.loginInfo = {}

load_components(Core)