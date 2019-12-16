from io import BytesIO
from django.shortcuts import HttpResponse,render,redirect
from utils.check_code import create_validate_code
from repository import models
from ..forms.account import LoginForm,RegisterForm
import json
from django.http import JsonResponse

def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img,code = create_validate_code()
    img.save(stream,'PNG')
    request.session['CheckCode']=code
    return HttpResponse(stream.getvalue())

def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method=='POST':
        result = {'status':False,'message':None,'data':None}
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            we= models.UserInfo.objects.all()
            print(we)
            user_info = models.UserInfo.objects.filter(username=username,password=password).values('username','password','blog__nid').first()
            print(user_info)
            if not user_info:
                result['message']='用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info']=user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60*60*24)
                # return render(request,'home.html')
        else:
            if 'check_code' in form.errors:
                result['message']='验证码过期'
            else:
                result['message']=form.errors
        return HttpResponse(json.dumps(result))

def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method=="GET":
        return render(request, 'register.html')
    elif request.method=="POST":
        form = RegisterForm(request=request, data=request.POST)
        ret = {'status': False, 'message': None, 'data': None}
        if form.is_valid():
            site=username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            title=nickname = form.cleaned_data.get('nickname')
            user_img = request.FILES.get('user_img')
            user = models.UserInfo.objects.filter(username=username)
            if user:
                ret['status'] = False
                ret['message'] = "该用户名已被占用"
            else:
                new_user = models.UserInfo.objects.create(**form.cleaned_data, avatar=user_img)
                models.Blog.objects.create(site=site, title=title, theme='哈哈哈', user=new_user)
                ret = {'status': True, 'message': '注册成功'}
        else:
            ret['status'] = False
            ret['message'] = form.errors
    return JsonResponse(json.dumps(ret), safe=False)



def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('/login.html')

