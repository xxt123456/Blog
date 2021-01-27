from ..auth.auth import check_login
from django.shortcuts import render, redirect
from repository import models
from django.http import JsonResponse
from utils.pagination import Pagination
from django.urls import reverse


@check_login
def tag(request, *args, **kwargs):
    """
    个人标签管理
    :param request:
    :return:
    """
    base_url = reverse('tag', kwargs=kwargs)
    blog = request.session.get('user_info')['blog__nid']
    if not blog:
        return redirect('/login')
    from django.db.models.aggregates import Count
    data_count = models.Tag.objects.filter(blog=blog).count()
    page_obj = Pagination(request.GET.get('p'), data_count)
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count('article2tag__article')).values().order_by('-nid')[
               page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)
    return render(request, 'backend_tag.html', {'tag_list': tag_list, 'page_str': page_str})


def del_tag(request):
    blog_id = request.session.get('user_info')['blog__nid']
    if request.method == 'POST':
        ds = request.POST.get('tag_id')
        models.Tag.objects.filter(nid=ds, blog=blog_id).delete()
        response = {'statu': True}
    return JsonResponse(response)


def add_tag(request):
    blog_id = request.session.get('user_info')['blog__nid']
    blog = models.Blog.objects.filter(nid=blog_id).select_related('user').first()
    if request.method == 'POST':
        tagname = request.POST.get('add_tag')
        if tagname == '':
            response = {'statu': False, 'res': '请输入类型'}
        else:
            models.Tag.objects.create(title=tagname, blog=blog)
            response = {'statu': True}
    return JsonResponse(response)


def edit_tag(request):
    blog_id = request.session.get('user_info')['blog__nid']
    tag_id = request.POST.get('tag_id')
    tag_title = request.POST.get('tag_title')
    models.Tag.objects.filter(nid=tag_id).update(title=tag_title, blog=blog_id)
    res = {'statu': True}
    return JsonResponse(res)
