import base64
import datetime as dt
import hmac
import requests
import json

APIKEY = "fbbecbb4-23e8-4d07-8042-34faf2f75a79"
APISECRET = "2124A0E2A73656FED8D2F62915877239"
PASS = "Iraydot-0508"
BASE_URL = 'https://aws.okx.com'

def send_signed_request(http_method, url_path, payload={}):
    '''
    See https://stackoverflow.com/questions/66486374/how-to-sign-an-okex-api-request
    '''

    def get_time():
        return dt.datetime.utcnow().isoformat()[:-3] + 'Z'

    def signature(timestamp, method, request_path, body, secret_key):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    # set request header
    def get_header(request='GET', endpoint='', body: dict = dict()):
        cur_time = get_time()
        header = dict()
        header['CONTENT-TYPE'] = 'application/json'
        header['OK-ACCESS-KEY'] = APIKEY
        header['OK-ACCESS-SIGN'] = signature(cur_time, request, endpoint , body, APISECRET)
        header['OK-ACCESS-TIMESTAMP'] = str(cur_time)
        header['OK-ACCESS-PASSPHRASE'] = PASS
        header['x-simulated-trading'] = '1'
        return header

    url = BASE_URL + url_path
    header = get_header(http_method, url_path, payload)
    response = requests.post(url, headers=header, data=payload)
    print(response.json())
    return response.json()

data = {
  "instId": "BTC-USDT",
  "tdMode": "cash",
  "side": "buy",
  "ordType": "limit",
  "px": "1000",
  "sz": "0.01"
}

res = send_signed_request("POST", "/api/v5/trade/order", payload=json.dumps(data))