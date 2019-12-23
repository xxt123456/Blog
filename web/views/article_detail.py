from django.shortcuts import render
from repository import models


def detail(request, site, nid):
    """
    博文详情页面及标签数据展示
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    tag_list = models.Tag.objects.filter(blog=blog)
    category = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,date_format(creat_time,"%%Y-%%m") as ctime from repository_article group by date_format(creat_time,"%%Y-%%m")'
    )
    article = models.Article.objects.filter(blog=blog, nid=nid).select_related('category', 'articledetail').first()
    return render(
        request,
        'article_detail.html',
        {
            'blog': blog,
            'category_list': category,
            'date_list': date_list,
            'article': article,
            'tag_list': tag_list
        }
    )
