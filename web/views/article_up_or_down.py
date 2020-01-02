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
        # 不存在点赞记录进行记录创建
        try:
            up_id = models.UpDown.objects.select_for_update().create(user_id=user_id, article_id=article_id,
                                                                     up=up_or_down)
            if up_id:
                from django.db.models import F
                if up_or_down == True:
                    models.Article.objects.select_for_update().filter(nid=article_id).update(up_count=F('up_count') + 1)
                    ret = {'status': 1, 'message': '点赞成功'}
                elif up_or_down == False:
                    models.Article.objects.select_for_update().filter(nid=article_id).update(
                        down_count=F('down_count') + 1)
                    ret = {'status': 2, 'message': '踩赞成功'}
        except Exception as e:
            print('2222', e)
    if up_or_down_id:
        try:
            """
            存在点赞记录:
            1、判断状态:传入为True
                （1）先判断之前的记录是True还是False，如果是True，则up_count减1；
                （2）先判断之前的记录是True还是False，如果是False，则返回“已踩赞，请勿点赞”
            2、如果是False，则down_down减1
                （1）先判断之前的记录是True还是False，如果是False，则down_down减1；
                （2）先判断之前的记录是True还是False，如果是True，则返回“已点赞，请勿踩赞”
            3、更新状态，删除文章点赞数
           """
            uo_or_down_stauts = models.UpDown.objects.filter(user_id=user_id, article_id=article_id).values(
                'up').first()
            from django.db.models import F
            if up_or_down == True and uo_or_down_stauts['up'] == True:
                models.Article.objects.select_for_update().filter(nid=article_id).update(up_count=F('up_count') - 1)
                models.UpDown.objects.select_for_update().filter(user_id=user_id, article_id=article_id).delete()
                ret = {'status': 3, 'message': '取消点赞'}
            if up_or_down == True and uo_or_down_stauts['up'] == False:
                ret = {'status': 4, 'message': '已踩赞，请勿点赞'}
            if up_or_down == False and uo_or_down_stauts['up'] == False:
                models.Article.objects.select_for_update().filter(nid=article_id).update(down_count=F('down_count') - 1)
                models.UpDown.objects.select_for_update().filter(user_id=user_id, article_id=article_id).delete()
                ret = {'status': 5, 'message': '取消踩暂'}
            if up_or_down == False and uo_or_down_stauts['up'] == True:
                ret = {'status': 6, 'message': '已点赞，请勿踩赞'}
        except Exception as e:
            print('11111', e)
    return JsonResponse(ret)
