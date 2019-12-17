from ..auth.auth import check_login
from django.shortcuts import render, redirect, HttpResponse
from repository import models
import uuid
import os
import json
from django.http import JsonResponse
from utils.pagination import Pagination
from django.urls import reverse


@check_login
def article(request, *args, **kwargs):
    """
    个人文章管理
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    blog_id = request.session.get('user_info')
    # blog_id = request.session.get(['user_info']['blog__nid'])

    condition = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v == '0':
            pass
        else:
            condition[k] = v
    condition['blog_id'] = blog_id['blog__nid']
    data_count = models.Article.objects.filter(**condition).count()
    page = Pagination(request.GET.get('p'), data_count)
    result = models.Article.objects.filter(**condition).order_by('-nid').only('nid', 'title', 'blog').select_related(
        'blog')[page.start:page.end]
    page_str = page.page_str(reverse('article', kwargs=kwargs))
    category_list = models.Category.objects.filter(blog_id=blog_id['blog__nid']).values('nid', 'title')
    type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choices)
    kwargs['p'] = page.current_page
    return render(
        request,
        'backend_article.html',
        {
            'result': result,
            'page_str': page_str,
            'category_list': category_list,
            'type_list': type_list,
            'arg_dict': kwargs,
            'data_count': data_count
        }
    )


@check_login
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    if request.method == 'GET':
        blog_id = request.session.get('user_info')['blog__nid']
        cat_list = models.Blog.objects.filter(nid=blog_id).values('category__title', 'category__nid', 'title', 'nid')
        tag_list = models.Blog.objects.filter(nid=blog_id).values('tag__title', 'tag__nid')
        return render(request, 'backend_add_article.html', {'cat_list': cat_list, 'tag_list': tag_list})
    title = request.POST.get('art_name')
    summary = request.POST.get('art_introduce')
    blog_id = models.Blog.objects.get(nid=request.POST.get('art_blog_id'))
    tags_id = models.Tag.objects.get(nid=request.POST.get('add_tag_id'))
    category_id = models.Category.objects.get(nid=request.POST.get('art_category_id'))
    article_type_id = 1
    art_content = request.POST.get('art_content')
    try:
        a = models.Article.objects.create(title=title, summary=summary, blog=blog_id, category=category_id,
                                          article_type_id=article_type_id)
        # models.Article2Tag.objects.create(article=a,tag=tags_id)
        res = {'status': True}
    except Exception as e:
        print(e)
        res = {'status': False, 'err': '添加失败'}
    return JsonResponse(res)


def del_article(request):
    """
    删除文章
    :param request:
    :return:
    """
    pass


def edit_article(request):
    """
    编辑文章
    :param request:
    :return:
    """
    pass
