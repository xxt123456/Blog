from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'repository'
    # 模板位置

    # 登录重定向
    login_url = '/login.html/'
    print('1111111111111111')
