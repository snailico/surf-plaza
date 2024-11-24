import requests

from .components import load_components

class Core(object):
    def __init__(self):
        self.alive, self.isLogging = False, False
        self.requests = requests.Session()
        self.uuid = None

load_components(Core)