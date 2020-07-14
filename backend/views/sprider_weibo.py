import requests
from bs4 import BeautifulSoup as bf

weibo_page = requests.get(url='https://weibo.com/',
                          headers={
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                              'cookie': 'Ugrow-G0=589da022062e21d675f389ce54f2eae7; SUB=_2AkMoURynf8NxqwJRmP4QxW7raIV-ygnEieKeDe18JRMxHRl-yT9jqhZetRB6A9EySIm74nS02g1Q2bZc9GZKWk-ATsat; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFywcJRYD2lH58Hn4ljrrEf; login_sid_t=85b97c5f85c281fa2e1181cfebf5adb7; cross_origin_proto=SSL; YF-V5-G0=f0aacce81fff76e1515ae68ac76a20c3; _s_tentry=passport.weibo.com; Apache=4310061478721.8984.1594725266738; SINAGLOBAL=4310061478721.8984.1594725266738; ULV=1594725266746:1:1:1:4310061478721.8984.1594725266738:; wb_view_log=1920*10801; WBStorage=42212210b087ca50|undefined; UOR=,,www.baidu.com',

                          })
weibo_page.encoding = 'utf-8'
ss = bf(weibo_page.text, 'lxml')
# s=ss.find_all(name='div',attrs={'id':'plc_main'})
s = ss.find_all('ul')

print(s)
