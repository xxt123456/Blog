import requests
import re
import random
from collections import defaultdict
from bs4 import BeautifulSoup as bf

proxies = {
    'http': 'http:113.204.164.194:8080',
}


def obj_url(url):
    obj = requests.get(url=url,
                       # proxies={'http',''},
                       headers={
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
                       })
    obj.encoding = 'gb2312'
    soup = bf(obj.text, 'lxml')
    return soup


def Spiderip(url):
    soup = obj_url(url)
    urls = soup.find_all(href=re.compile('page'))  # 获取当前代理url列表
    ip_list = []  # 有效ip代理
    for url in urls:
        url = ('http://www.ip3366.net/free/' + url['href'])
        soup = obj_url(url)

        # 一个key对应多个value
        proxies = defaultdict(list)
        trs = soup.find('table').find('tbody').find_all('tr')
        for obj_td in trs:
            tds = obj_td.find_all('td')
            ip = tds[0].text
            port = tds[1].text
            protcol = tds[3].text.lower()
            location = tds[4].text
            ip_response = tds[5].text
            update = tds[6].text
            proxies[protcol].append(protcol + ":" + ip + ":" + port)

            for i in proxies[protcol]:
                proxie = {}
                proxie[protcol] = i
                if i not in ip_list:

                    try:
                        effective = requests.get(url='https://www.baidu.com', proxies=proxie, timeout=2)
                        if effective.status_code == 200:
                            print('1111', effective, i)
                            # with open('../../static/11.txt', 'a') as f:
                            ip_list.append(i)
                            # f.write(str(i) + '\n')

                    except Exception as e:
                        print('出现异常', e)
                    # return ip, port, protcol, location, ip_response, update
                return ip_list

# Spiderip('http://www.ip3366.net/free')
