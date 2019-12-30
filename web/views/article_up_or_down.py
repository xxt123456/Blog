from django.shortcuts import render, HttpResponse
from repository import models
from django.http import JsonResponse

from django.db import transaction


@transaction.atomic
def artilce_give(request):
    """
    点赞
    :param request:
    :return:
    """
    user_id = request.POST.get('user_id')
    article_id = request.POST.get('article_id')
    up_or_down = bool(int(request.POST.get('up_or_down')))
    up_or_down_id = models.UpDown.objects.filter(user_id=user_id, article_id=article_id)
    ret = {'status': None, 'message': None}
    if not up_or_down_id:
        try:
            up_id = models.UpDown.objects.select_for_update().create(user_id=user_id, article_id=article_id,
                                                                     up=up_or_down)
            if up_id:
                from django.db.models import F
                if up_or_down == True:
                    models.Article.objects.select_for_update().filter(nid=article_id).update(up_count=F('up_count') + 1)
                    ret = {'status': True, 'message': '点赞成功'}
                elif up_or_down == False:
                    models.Article.objects.select_for_update().filter(nid=article_id).update(
                        down_count=F('down_count') + 1)
                    ret = {'status': True, 'message': '踩赞成功'}
        except Exception as e:
            print('2222', e)
    if up_or_down_id:
        try:
            models.UpDown.objects.select_for_update().filter(user_id=user_id, article_id=article_id).delete()
            from django.db.models import F
            if up_or_down == True:
                models.Article.objects.select_for_update().filter(nid=article_id).update(up_count=F('up_count') - 1)
                ret = {'status': True, 'message': '取消点赞'}
            elif up_or_down == False:
                models.Article.objects.select_for_update().filter(nid=article_id).update(down_count=F('down_count') - 1)
                ret = {'status': True, 'message': '取消踩暂'}
        except Exception as e:
            print('11111', e)
    return JsonResponse(ret)
