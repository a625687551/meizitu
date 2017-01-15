import random
import pandas as pd
from sqlalchemy import create_engine
from meizitu import settings

'''
这个类主要产生随机的IP
'''
class RandomProxy(object):
    def __init__(self):#初始化IP池
        dbfile = r'D:/GitHub/IPProxyPool/IPProxyPool_py3/data/proxy.db'
        db_conn = create_engine('sqlite:///' + dbfile)
        df = pd.read_sql('select * from proxys', db_conn)
        df.update(df.port.map(str))
        self.iplist = list('http://' + df.ip + ':' + df.port)
        # print(self.iplist)
    def process_request(self,request,spider):
        '''
        在请求上添加代理
        ：:param request
        :param spider
        :return
        '''

        ip = random.choice(self.iplist)
        # ip = 'http://188.0.25.152:8081'
        # result = self.db_helper.findOneResult({'proxyId':ip})
        request.meta['proxy'] =ip
# #test code
# tl=RandomProxy()
# print(tl.iplist)