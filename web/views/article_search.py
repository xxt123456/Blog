from django.shortcuts import render, redirect, HttpResponse
from repository import models
from django.http import JsonResponse


def search(request):
    """
    搜索
    :return:
    """
    # 本地文章搜索
    search_key = request.POST.get('search_text')
    ret = {'status': None, 'message': None}
    # 未输入任何值进行搜索
    if not search_key:
        ret['status'] = 0
        ret['message'] = '请输入搜索数据'
    # 输入指定数据进行模糊搜索
    else:
        search_object = models.Article.objects.filter(title__icontains=search_key).values('title', 'summary')
        print(search_object)
        ret['status'] = 1
        ret['message'] = list(search_object)
        print(ret['message'])

    return JsonResponse(ret)
