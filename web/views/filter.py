from django.shortcuts import render, redirect
from repository import models


def filter(request, site, condition, val):
    """
    分类显示：博客类别展示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/login')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,date_format(creat_time,"%%Y-%%m") as ctime from repository_article group by date_format(creat_time,"%%Y-%%m")'
    )
    template_name = "article_summary_list.html"
    if condition == 'tag':
        # 通过tag进行分类的文章列表
        article_list = models.Article.objects.filter(tags=val, blog=blog).all()
    elif condition == 'category':
        # 通过category进行分类的文章列表
        article_list = models.Article.objects.filter(category=val, blog=blog).all()
    elif condition == 'date':
        # 通过data进行分类的文章列表
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['date_format(creat_time,"%%Y-%%m")=%s'], params=[val, ]).all()
    else:
        article_list = []

    return render(
        request,
        template_name,
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )
