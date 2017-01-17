import random
import pandas as pd
import re
from sqlalchemy import create_engine
from meizitu import settings
from scrapy.http.request import Request
import requests
'''
这个类主要产生随机的IP
'''
class RandomProxy(object):
    def __init__(self):#初始化IP池
        #调用本地IP池子选出的IP
        # dbfile = r'D:/GitHub/IPProxyPool/IPProxyPool_py3/data/proxy.db'
        # db_conn = create_engine('sqlite:///' + dbfile)
        # df = pd.read_sql('select * from proxys', db_conn)
        # df.update(df.port.map(str))
        # self.iplist = list('http://' + df.ip + ':' + df.port)
        # print(self.iplist)

        #调用网站上提供的免费IP
        self.iplist=[]
        db_content=requests.get(url='http://haoip.cc/tiqu.htm')
        # iplistb=re.findall(r'r/>(.*?)<br/>',db_content.text,re.S)
        iplistb = re.findall('([0-9.]+:[0-9]+)<br/>', db_content.text, re.S)
        for i in iplistb:
            self.iplist.append('http://'+re.sub('\n','',i).strip())
        # test code
        # print(type(random.choice(self.iplist)))
        print(len(self.iplist),self.iplist)
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
#test code
tl=RandomProxy()


