from django.shortcuts import render
from repository import models


def commnet(request, *args, **kwargs):
    user_id = request.POST.get('user_id')
    content = request.POST.get('content')
    article_id = request.POST.get('article')
    parent_comment_id = request.POST.get('parent_comment_id')
    article = models.Article.objects.filter(nid=article_id)
    if article_id:
        models.Comment.objects.create(content=content, article=article_id, parent_comment=parent_comment_id,
                                      user=user_id)
