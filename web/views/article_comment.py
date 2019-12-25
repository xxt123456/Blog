from django.shortcuts import render, HttpResponse
from repository import models
from django.http import JsonResponse


def article_commnet(request):
    user_id = request.POST.get('user_id')
    content = request.POST.get('com_content')
    article_id = request.POST.get('article_id')
    parent_comment_id = request.POST.get('parent_comment_id')
    if not parent_comment_id:
        article = models.Article.objects.get(nid=article_id)
        user = models.UserInfo.objects.get(nid=user_id)
        if article and user:
            models.Comment.objects.create(content=content, article=article, user=user)
            from django.db.models import F
            models.Article.objects.filter(nid=article_id).update(comment_count=F('comment_count') + 1)
            ret = {'status': True, 'message': '评论成功'}
    return JsonResponse(ret)
