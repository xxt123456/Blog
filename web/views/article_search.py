from django.shortcuts import render, redirect, HttpResponse
from repository import models
from django.http import JsonResponse
from backend.views.proxy import Spiderip
from backend.views.sprider_weibo import WeiBo_Hot


def search(request):
    """
    搜索
    :return:
    """
    # 本地文章搜索
    search_key = request.POST.get('search_text')
    sprider_search = request.POST.get('sprider_search')
    sprider_weibo_search = request.POST.get('sprider_weibo_search')
    sprider_weibo_search_obj = []
    if sprider_weibo_search:
        weibo_obj = sprider_weibo_search.split(',', 1)
        if len(weibo_obj) > 1:
            if int(weibo_obj[1]) > 10:
                sprider_weibo_search = 10
            else:
                sprider_weibo_search = int(weibo_obj[1])
        else:
            sprider_weibo_search = []
            sprider_weibo_search_obj = weibo_obj[0]
    ret = {'status': None, 'message': None}
    # 未输入任何值进行搜索
    if not (search_key or sprider_search or sprider_weibo_search or sprider_weibo_search_obj):
        ret['status'] = 0
        ret['message'] = '请输入搜索数据'

    # 爬代理ip
    elif sprider_search:
        serach_objs = Spiderip(sprider_search)
        for sprider in serach_objs:
            ip = sprider.split(':')[1]
            port = sprider.split(':')[2]
            protcol = sprider.split(':')[0]
            models.Proxy_Pool.objects.create(ip=ip, port=port, protcol=protcol)
        sprider_obj = models.Proxy_Pool.objects.filter().values('protcol', 'ip', 'port').order_by('-id')[:10]
        ret['status'] = 3
        ret['message'] = list(sprider_obj)

        return JsonResponse(ret)
    # 爬微博热搜

    elif sprider_weibo_search:
        weibo_serach = WeiBo_Hot(sprider_weibo_search)
        ret['status'] = 4
        ret['message'] = weibo_serach
        return JsonResponse(ret)
    # 爬微博指定内容
    elif sprider_weibo_search_obj:
        weibo_serach = WeiBo_Hot(1, sprider_weibo_search_obj)
        ret['status'] = 5
        ret['message'] = weibo_serach
        return JsonResponse(ret)
    # 输入指定数据进行模糊搜索
    else:
        search_object = models.Article.objects.filter(title__icontains=search_key).values('nid', 'title', 'summary',
                                                                                          'blog__site')
        if not search_object:
            ret['status'] = 1
            ret['message'] = '查询数据为空'
            return JsonResponse(ret)
        ret['status'] = 2
        ret['message'] = list(search_object)

    return JsonResponse(ret)

