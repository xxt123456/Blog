from django.shortcuts import render, redirect
from repository import models

def home(request,site):
    """
    个人博客web首页
    :param request:
    :param site:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/all/0.html')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,date_format(creat_time,"%%Y-%%m") as ctime from repository_article group by date_format(creat_time,"%%Y-%%m")'
    )
    article_list = models.Article.objects.filter(blog=blog).order_by('nid').all()
    return render(
        request,
        'home.html',
        {
            'blog':blog,
            'tag_list':tag_list,
            'category_list':category_list,
            'date_list':date_list,
            'article_list':article_list
        }
    )
