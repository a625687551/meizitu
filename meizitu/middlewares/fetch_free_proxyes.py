#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import logging

logger = logging.getLogger(__name__)

def get_html(url):#获取网页
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36"}
    html=requests.get(url,headers=headers)
    return html.text
def get_soup(url):
    soup = BeautifulSoup(get_html(url), "lxml")
    return soup

def fetch_kxdaili(page):
    """
    从www.kxdaili.com抓取免费代理
    """
    proxyes = []
    try:
        url = "http://www.kxdaili.com/dailiip/1/%d.html" % page
        soup = get_soup(url)
        table_tag = soup.find("table", attrs={"class": "segment"})
        trs = table_tag.tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text.split(" ")[0]
            if float(latency) < 1: # 输出延迟小于1秒的代理
                proxy = "%s:%s" % (ip, port)
                proxyes.append(proxy)
    except:
        logger.warning("fail to fetch from kxdaili")
    return proxyes

# def img2port(img_url):##调整 这个代理不能用了
#     """
#     mimvp.com的端口号用图片来显示, 本函数将图片url转为端口, 目前的临时性方法并不准确
#     """
#     code = img_url.split("=")[-1]
#     if code.find("AO0OO0O")>0:
#         return 80
#     else:
#         return None

def fetch_mimvp():
    """
    从http://haoip.cc/tiqu.htm抓免费代理
    """
    proxyes = []
    try:
        url = "http://haoip.cc/tiqu.htm"
        soup = get_html(url)
        table = re.findall('([0-9.]+:[0-9]+)<br/>', soup, re.S)
        for i in table:
            proxy=re.sub('\n', '', i).strip()
            proxyes.append(proxy)
    except:
        logger.warning("fail to fetch from haoip")
    return proxyes

def fetch_xici():
    """
    http://www.xicidaili.com/nn/
    """
    proxyes = []
    try:
        url = "http://www.xicidaili.com/nn/"
        soup = get_soup(url)
        table = soup.find("table", attrs={"id": "ip_list"})
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[1].text
            port = tds[2].text
            speed = tds[6].div["title"][:-1]
            latency = tds[7].div["title"][:-1]
            if float(speed) < 3 and float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from xici")
    return proxyes

def fetch_ip181():
    """
    http://www.ip181.com/
    """
    proxyes = []
    try:
        url = "http://www.ip181.com/"
        soup = get_soup(url)
        table = soup.find("table")
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text[:-2]
            if float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except Exception as e:
        logger.warning("fail to fetch from ip181: %s" % e)
    return proxyes

def fetch_httpdaili():
    """
    http://www.httpdaili.com/mfdl/
    更新比较频繁,网页编码有问题没有解决
    """
    proxyes = []
    try:
        url = "http://www.httpdaili.com/mfdl/"
        soup = get_soup(url)
        table = soup.find("div", attrs={"kb-item-wrap11"})
        trs = table.find_all("tr")[1:]
        for i in range(1, len(trs)+1):
            try:
                tds = trs[i].find_all("td")
                ip = tds[0].text
                port = tds[1].text
                type = tds[2].text
                proxyes.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes

def fetch_66ip():
    """    
    http://www.66ip.cn/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    proxyes = []
    try:
        # 修改getnum大小可以一次获取不同数量的代理
        url = "http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip"
        content = get_html(url)
        # urls = content.split("</script>")[-1].split("<br />")
        urls = re.findall('([0-9.]+:[0-9]+)<br />',content, re.S)
        for u in urls:
            if u.strip():
                proxyes.append(u.strip())
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes

    

def check(proxy):
    import requests
    url='http://www.mzitu.com/'
    # url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"

    # proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    # opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
    # try:
    #     response = opener.open(url,timeout=3)
    #     return response.code == 200 and response.url == url
    # except Exception:
    #     return False
    proxies={'http': "http://" + proxy}
    try:
        test = requests.get(url, proxies=proxies, timeout=10)
        return test.status_code==200 and test.url==url
    except Exception:
        return False


def fetch_all(endpage=9):
    proxyes = []
    for i in range(1, endpage):
        proxyes += fetch_kxdaili(i)
    proxyes += fetch_mimvp()
    proxyes += fetch_xici()
    proxyes += fetch_ip181()
    proxyes += fetch_httpdaili()
    proxyes += fetch_66ip()
    valid_proxyes = []
    logger.info("checking proxyes validation")
    print(u'检测数量是',len(proxyes),proxyes)
    for p in proxyes:
        if check(p):
            valid_proxyes.append(p)
            print(p)
    return valid_proxyes

if __name__ == '__main__':
    import sys
    root_logger = logging.getLogger("")
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(name)-8s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    proxyes = fetch_all()
    #print check("202.29.238.242:3128")
    for p in proxyes:
        print(p,'可用')
