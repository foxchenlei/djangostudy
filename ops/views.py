from django.shortcuts import render,render_to_response,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.views import defaults
from django.views.generic import View
from . import models
from . import forms


# Create your views here.
import hashlib
import datetime
import pytz
from django.conf import settings

def hash_code(s, salt='emar'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.foxchan.com的测试邮件'
    text_content = '欢迎访问www.foxchan.com，这里是foxchan的站点，专注于Python和Django技术的分享！'
    html_content = '''
                   <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.foxchan.com</a>，
                   这里是foxchan站点，专注于Python和Django技术的分享！</p>
                   <p>请点击站点链接完成注册确认！</p>
                   <p>此链接有效期为{}天！</p>
                   '''.format('101.254.242.12:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def index(r):
    pass
    return render(r, 'ops/index.html')

#django form

def login(r):
    if r.session.get('is_login',None):
       return redirect("/index/")
    if r.method == "POST":
       login_form = forms.UserForm(r.POST)
       message = "请检查填写的内容！"
       if login_form.is_valid():
          username = login_form.cleaned_data['username']
          password = login_form.cleaned_data['password']
          try:
              user = models.User.objects.get(name=username)
              if not user.has_confirmed:
                 message = "该用户还未通过邮件确认！"
                 return render(r, 'ops/login.html', locals())

              if user.password == hash_code(password): # 哈希值和数据库内的值进行比对
                 r.session['is_login'] = True
                 r.session['user_id'] = user.id
                 r.session['user_name'] = user.name
                 return redirect('/index/')
              else:
                 message = "密码不正确！"
          except:
              message = "用户不存在！"
       return render(r, 'ops/login.html', locals())
    login_form = forms.UserForm()
    return render(r, 'ops/login.html', locals())

#html表单的写法
#def login(r):
#    if r.method == "POST":
#        username = r.POST.get('username', None)
#        password = r.POST.get('password', None)
#        message = "所有字段都必须填写"
#        if username and password:
#           username = username.strip()
#           try:
#              user = models.User.objects.get(name=username)
#              if user.password == password:
#              	 return redirect("/index/")
#              else:
#                 message = "密码不正确！！"
#           except:
#              message = "用户名不存在！！"
#        return render(r, 'ops/login.html', {"message": message})
#    return render(r, 'ops/login.html')

def register(r):
    if r.session.get('is_login', None):
       # 登录状态不允许注册。你可以修改这条原则！
       return redirect("/index/")
    if r.method == "POST":
       register_form = forms.RegisterForm(r.POST)
       message = "请检查填写的内容！"
       if register_form.is_valid():  # 获取数据
          username = register_form.cleaned_data['username']
          password1 = register_form.cleaned_data['password1']
          password2 = register_form.cleaned_data['password2']
          email = register_form.cleaned_data['email']
          sex = register_form.cleaned_data['sex']
          if password1 != password2:  # 判断两次密码是否相同
             message = "两次输入的密码不同！"
             return render(r, 'ops/register.html', locals())
          else:
             same_name_user = models.User.objects.filter(name=username)
             if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
                return render(r, 'ops/register.html', locals())
             same_email_user = models.User.objects.filter(email=email)
             if same_email_user:  # 邮箱地址唯一
                message = '该邮箱地址已被注册，请使用别的邮箱！'
                return render(r, 'ops/register.html', locals())
             # 当一切都OK的情况下，创建新用户
             new_user = models.User()
             new_user.name = username
             new_user.password = hash_code(password1) # 使用加密密码
             new_user.email = email
             new_user.sex = sex
             new_user.save()
             
             code = make_confirm_string(new_user)
             send_email(email, code)

             message = '请前往注册邮箱，进行邮件确认！'
             return render(r,'ops/confirm.html', locals())  #跳转到等待邮件确认页面。
    register_form = forms.RegisterForm()
    return render(r, 'ops/register.html', locals())

def user_confirm(r):
    code = r.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(r, 'ops/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
       confirm.user.delete()
       message = '您的邮件已经过期！请重新注册!'
       return render(r, 'ops/confirm.html', locals())

    else:
       confirm.user.has_confirmed = True
       confirm.user.save()
       confirm.delete()
       message = '感谢确认，请使用账户登录！'
       return render(r, 'ops/confirm.html', locals())

def logout(r):
    if not r.session.get('is_login', None):
       return redirect("/index/")
    r.session.flush()
    return redirect("/index/")


def simplemap(request):
    rst = "hello world"
    html = "<html><body><h1> my first word is {0}</h1></body></html>".format(rst)
    return HttpResponse(html)

def my404(r):
    rst = "this is custom 404 page"
    
    return defaults.page_not_found(r, Exception)


def paramap(req, year):
    rst = "THis year is {0}".format(year)
    return HttpResponse(rst)

def index_1(req, p1, p2):
    rst = "this is first para:{0}, this is second para:{1}".format(p1,p2)
    return HttpResponse(rst)

def index_2(req, pn):
    rst = "this is first para:{0}".format(pn)
    return HttpResponse(rst)

def extra(req, author, version):
    rst = "All right by {0}, the current version is {1} ".format(author, version)
    return HttpResponse(rst)


def redit_1(request):
    return HttpResponseRedirect("/dest")

def redit_2(request):
    return HttpResponseRedirect(reverse("d1"))

def dest(request):
    rst = "dest page"
    return  HttpResponse(rst)

def getinfo(request):
    rst = ''
    for k, v in request.GET.items():
      rst += k + '-->' + v
      rst += ','

    return HttpResponse("get value of request is {0}".format(rst))


def post_get(r):
    html = """
         <html>
           <head>
             <title>测试post</title>
           </head>
           <body>
             <form method="post" action="/post_post/">
                   姓名:<input type="text" name="username"/></br>
                   密码:<input type="password" name="password"/></br>
                   性别:<input type="radio" name="ugender" value="1"/>男
                        <input type="radio" name="ugender" value="0"/>女</br>
                   爱好:<input type="checkbox" name="hobby" value="胸口碎大石"/>胸口碎大石
                   <input type="checkbox" name="hobby" value="喝酒"/>喝酒
                   <input type="checkbox" name="hobby" value="跳楼"/>跳楼
                   <input type="checkbox" name="hobby" value="看美女"/>看美女</br>
                   <input type="submit" value="提交"/>
           </body>
         </html>
    """
    return HttpResponse(html)
def post_post(r):
    rst = ''
    for k, v in r.POST.items():
      rst += k + '-->' + v
      rst += ','

    return HttpResponse("get value of post is {0}".format(rst))


def myrender(r):
    rsp = render(r, "render.html")
    return rsp


def myrender_to_rsp(r):
    rsp = render("render.html")
    return rsp

def myredirect(r):
    print ("i am redirect page")
    return redirect(reverse("d1"))

class MyView(View):

    def get(self, request):
        rst = "hello from myview"
        return  HttpResponse(rst)
