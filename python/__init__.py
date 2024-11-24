# import io, os,subprocess
# import qrcode
# import requests
 
# # 图片的URL
# url = 'https://login.weixin.qq.com/qrcode/gZboS5NtJw=='
 
# # 发送GET请求获取图片内容
# response = requests.get(url)
 
# # 检查请求是否成功
# if response.status_code == 200:
#     # 打开文件进行二进制写入
#     with open('QR.png', 'wb') as f:
#         f.write(response.content)
#     print('图片保存成功')
# else:
#     print('请求图片失败，状态码:', response.status_code)

 
# # img = qrcode.make('https://login.weixin.qq.com/qrcode/YfClsW9kSw==')
# # img.save("QR.png")
 
# subprocess.call(['open', "QR.png"])
from .core import Core
 
instanceList = []

def new_instance():
    newInstance = Core()
    instanceList.append(newInstance)
    return newInstance