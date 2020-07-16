import time
import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bf

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
# browser=webdriver.Chrome()
browser.get('https://weibo.com/')
time.sleep(8)


# weibo_page = requests.get(url='https://weibo.com/',
#                           headers={
#                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
#                               'cookie': 'Ugrow-G0=589da022062e21d675f389ce54f2eae7; SUB=_2AkMoURynf8NxqwJRmP4QxW7raIV-ygnEieKeDe18JRMxHRl-yT9jqhZetRB6A9EySIm74nS02g1Q2bZc9GZKWk-ATsat; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFywcJRYD2lH58Hn4ljrrEf; login_sid_t=85b97c5f85c281fa2e1181cfebf5adb7; cross_origin_proto=SSL; YF-V5-G0=f0aacce81fff76e1515ae68ac76a20c3; _s_tentry=passport.weibo.com; Apache=4310061478721.8984.1594725266738; SINAGLOBAL=4310061478721.8984.1594725266738; ULV=1594725266746:1:1:1:4310061478721.8984.1594725266738:; wb_view_log=1920*10801; WBStorage=42212210b087ca50|undefined; UOR=,,www.baidu.com',
#
#                           })
# weibo_page.encoding = 'utf-8'
# ss = bf(weibo_page.text, 'lxml')
# s=ss.find_all(name='div',attrs={'id':'plc_unlogin_home_main'})
# s = ss.find_all('ul')
weibo_pages = bf(browser.page_source, 'lxml')
weibo_page = weibo_pages.find_all(name='div', attrs={'id': 'pl_unlogin_home_feed'})
for title in weibo_page:
    # title_list = weibo_page.find_all(name='ul', attrs={'node-type': 'feed_list'})
    # title_list = weibo_page.find_all(name='div', attrs={'class': 'UG_list_v2 clearfix'})
    list_imgA = title.find_all('div', attrs={'action-type': 'feed_list_item', 'class': 'UG_list_a'})
    list_imgB = title.find_all('div', attrs={'action-type': 'feed_list_item', 'class': 'UG_list_b'})
    list_imgC = title.find_all('div', attrs={'action-type': 'feed_list_item', 'class': 'UG_list_c'})
    # for obj in title_list:
    #     print('333333333',obj)
    #     # print('2222',obj.findAll('div',attrs={'action-type': 'feed_list_item'}))
    #     video = obj.find(attrs={'node-type': re.compile(r'fl_h5_video$')})
    #     list_imgA = obj.find('div',attrs={'class': 'UG_list_a'})
    #     list_imgB = obj.find('div',attrs={'class': 'UG_list_b'})
    #     list_imgC = obj.find('div',attrs={'class': 'UG_list_c'})
    #     print('1111111',video)
    #     print('1333333',list_imgA)
    #     print('122222',list_imgA)
    #     print('144444444',list_imgA)
    # # 微博内容为视频时
    # if video:
    #     img = video.find('img').get('src')  # 视频照片地址
    #     href = obj.find('h3').find('a', attrs={'extra-data': 'type=topic'})  # 博文链接
    #     face = obj.find('span', attrs={'class': 'subinfo_face'}).find('img').get('src')  # 博主头像

    if list_imgA:
        for list_img in list_imgA:
            # title = obj.find('h3').text  # 博文主题
            imgs = list_img.find('div', attrs={'class': 'list_nod clearfix'}).findAll('img')
            href = list_img.find('h3').find('a', attrs={'extra-data': 'type=topic'})  # 博文链接
            face = list_img.find('span', attrs={'class': 'subinfo_face'}).find('img').get('src')  # 博主头像
            for img in imgs:
                # print('123',imgs)
                # print('1234',len(imgs))
                # img = img.find('img').get('src')  # 微博照片
                print('AAA', img.get('src'))
    if list_imgB:
        for list_img in list_imgB:
            # print('BBBB',list_img)
            img = list_img.find('div', attrs={'class': 'pic W_piccut_h'}).find('img').get('src')
            print('BBBB', img)
    #
    if list_imgC:
        for list_img in list_imgC:
            print('ccccc', list_img)
            img = list_img.find('div', attrs={'class': 'pic W_piccut_v'}).find('img').get('src')
            print('CCCC', img)
    # title = title.find('h3').text  # 博文主题
    # try:
    #     username = title.find('span', attrs={'class': 'subinfo S_txt2'}).text  # 博主昵称
    # except AttributeError as e:
    #     pass
    # print(e)

    # print(username)


browser.quit()
