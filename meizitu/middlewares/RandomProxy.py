import random
import pandas as pd
import re
import json
from sqlalchemy import create_engine
from meizitu import settings
from scrapy.http.request import Request
import requests
'''
这个类主要产生随机的IP
'''
class RandomProxy(object):
    def __init__(self):
        '''
        初始化IP pool
        '''
        self.iplist=[]
        r=requests.get(url='http://127.0.0.1:8000/?count=20&country=国内')
        ip_ports = json.loads(r.text)
        # for i in ip_ports:
        #     self.iplist.append('http://'+re.sub('\n','',i).strip())
        for i in ip_ports:
            self.iplist.append('http://'+str(i[0])+':'+str(i[1]))

        # test code
        # print(type(random.choice(self.iplist)))
        # print(len(self.iplist),self.iplist)
        # print(ip_ports)
    def process_request(self,request,spider):
        '''
        在请求上添加代理
        '''
        ip = random.choice(self.iplist)
        request.meta['proxy'] =ip
        # #如果有代理需要账号密码话
        # proxy_user_pass='USERNAME:PASSWORD'
        # # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
    def process_response(self,request,response,spider):
        '''
        检查response.status, 根据status是否在允许的状态码中决定是否切换到下一个proxy, 或者禁用proxy
        '''
        if response.status != 200:
            new_request = request.copy()
            new_request.dont_filter = True
            print(u'更换代理',response.meta.get('proxy','localhost'))
            return new_request
        else:
            return response
#test code
# tl=RandomProxy()


