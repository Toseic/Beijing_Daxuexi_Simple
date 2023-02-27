import random

import requests
from lxml import etree
from requests import head

ss = requests.session()
ua_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
]


def headers():
    return {'User-Agent': random.choice(ua_list),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'}

def proxies(proxy):
    return {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
    }

def catchProxy():
    """
    https://scrapingant.com/free-proxies/#free-proxy-list-for-web-scraping-and-web-surfing
    api: https://scrapingant.com/proxies
    """
    print('catch work begin')

    proxies = []
    url = 'https://scrapingant.com/proxies'
    resp = ss.get(url)
    tree = etree.HTML(resp.content)
    mlist = tree.xpath('//table/tr')
    for tr in mlist:
        xph = tr.xpath('./td/text()')
        if xph:
            proxies.append(f"{xph[0]}:{xph[1]}")
    print('catch work done')
    return proxies


def testProxy(proxy):
    testurl = 'https://m.bjyouth.net/site/login'
    try:
        r = head(url=testurl, headers=headers(), proxies=proxies(proxy), timeout=3)
        return True if r.status_code == 200 else False
    except Exception as e:
        # print(e)
        return False


def fetchproxy():
    print("fetching proxies ...")
    useful_l = []
    for proxy in catchProxy()[:50]:
        if testProxy(proxy):
            print(f"\nsuccessfully get proxy: {proxy}")
            useful_l.append(proxy)
        else:
            print('.',end='')

    if len(useful_l):
        return useful_l
    return False



if __name__ == "__main__":
    print(fetchproxy())