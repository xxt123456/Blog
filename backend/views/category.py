from ..auth.auth import check_login
from django.shortcuts import render, redirect
from repository import models
from django.http import JsonResponse
from utils.pagination import Pagination
from django.urls import reverse


@check_login
def category(request, *args, **kwargs):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    bass_url = reverse('category', kwargs=kwargs)
    blog_id = request.session.get('user_info')['blog__nid']
    if not blog_id:
        return redirect('/login')
    date_count = models.Category.objects.filter(blog=blog_id).count()
    page_obj = Pagination(request.GET.get('p'), date_count)
    from django.db.models.aggregates import Count
    date_list = models.Category.objects.filter(blog=blog_id).annotate(c=Count('article__title')).values('title', 'c',
                                                                                                        'nid')[
                page_obj.start:page_obj.end]
    page_str = page_obj.page_str(bass_url)
    return render(request, 'backend_category.html', {'date_list': date_list, 'page_str': page_str})


def add_category(request):
    blog_id = request.session.get('user_info')['blog__nid']
    blog = models.Blog.objects.filter(nid=blog_id).first()
    add_cate = request.POST.get('add_cate')
    if add_cate == '':
        res = {'statu': False, 'res': '请输入分类类型'}
    else:
        models.Category.objects.create(title=add_cate, blog=blog)
        res = {'statu': True}
    return JsonResponse(res)


def del_category(request):
    del_cate_id = request.POST.get('cate_id')
    try:
        models.Category.objects.filter(nid=del_cate_id).delete()
        res = {'statu': True}
    except Exception as err:
        res = {'statu': False, 'res': '删除异常'}
    return JsonResponse(res)


def edit_category(request):
    blog_id = request.session.get('user_info')['blog__nid']
    category_title = request.POST.get('cate_title')
    category_id = request.POST.get('cate_id')
    try:
        models.Category.objects.filter(nid=category_id).update(title=category_title, blog=blog_id)
        res = {'statu': True}
    except Exception as err:

        res = {'statu': False, 'res': '修改失败'}
    return JsonResponse(res)
