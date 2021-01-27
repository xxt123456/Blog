from ..auth.auth import check_login
from django.shortcuts import render, HttpResponse
from repository import models
import uuid
import os
import json


@check_login
def index(request):
    if request.method =="GET":
        user_info=request.session.get('user_info')
        if not user_info['blog__nid']:
            models.Blog.objects.create()
    return render(request, 'backend_index.html')

@check_login
def base_info(request):
    """
    个人信息
    :param request:
    :return:
    """
    current_username = request.session.get('user_info')

    email = models.UserInfo.objects.filter(username=current_username['username']).values('email', 'nickname', 'avatar',
                                                                                         'username')
    return render(request, 'backend_base_info.html',
                  {'current_username': current_username, 'email': email})



@check_login
def upload_avatar(request):
    '''
    用户头像
    :param request:
    :return:
    '''
    ret = {'status':False,'data':None,'message':None}
    if request.method == 'POST':
        username = request.POST.get('username')
        file_obj = request.FILES.get('img_upload')
        if not file_obj:
            pass
        else:
            file_name = ''.join(str(uuid.uuid4()).split('-')) + '.' + str(file_obj).split('.', -1)[-1]
            file_path = 'static/imgs/avatar/' + username + '/'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            with open(file_path + file_name, 'wb') as f:
                for i in file_obj:
                    f.write(i)
            # for chunk in file_obj.chunks():
            #     f.write(chunk)
            # f.close()
            models.UserInfo.objects.filter(username=username).update(avatar=file_name)
            ret['status']=True
            ret['data']=file_path
    return HttpResponse(json.dumps(ret))

