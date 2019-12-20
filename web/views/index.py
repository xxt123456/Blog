from django.shortcuts import HttpResponse, render, redirect
from repository import models
from django.urls import reverse
from utils.pagination import Pagination


def index(request, *args, **kwargs):
    """
    博客首页
    :param request:
    :return:
    """
    article_type_list = models.Article.type_choices
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        bass_url = reverse('index', kwargs=kwargs)
    else:
        article_type_id = None
        bass_url = '/'
    data_count = models.Article.objects.filter(**kwargs).count()
    if not data_count:
        data_count = 1
    if article_type_id == 0:
        data_count = models.Article.objects.all().order_by('nid').count()
        page_obj = Pagination(request.GET.get('p'), data_count)
        article_list = models.Article.objects.all().order_by('nid')[page_obj.start:page_obj.end]
    else:
        page_obj = Pagination(request.GET.get('p'), data_count)
        article_list = models.Article.objects.filter(**kwargs).order_by('nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(bass_url)

    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_list': article_type_list,
            'article_type_id': article_type_id,
            'page_str': page_str
        }
    )
