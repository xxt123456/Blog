from django.shortcuts import render, redirect, HttpResponse
from repository import models
from django.http import JsonResponse
from backend.views.proxy import Spiderip


def search(request):
    """
    搜索
    :return:
    """
    # 本地文章搜索
    search_key = request.POST.get('search_text')
    sprider_search = request.POST.get('sprider_search')
    ret = {'status': None, 'message': None}
    # 未输入任何值进行搜索
    if not (search_key or sprider_search):
        ret['status'] = 0
        ret['message'] = '请输入搜索数据'

    # 爬虫
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
        # return HttpResponse('100')
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
        # print(ret['message'])

    return JsonResponse(ret)

