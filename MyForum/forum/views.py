from urllib import request
from django.urls import reverse
from sys import float_repr_style
from django.db import IntegrityError
from django.shortcuts import render
from pkg_resources import require

from .models import Collection,  User, Posting, Comment, Like
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# Create your views here.

#网站入口，登录或闲逛或注册
def entry(request):
    return render(request,'entry.html') 

#首页，展示近期的帖子
def index(request):
    user=request.user
    postings=Posting.objects.filter(p_See=1).all().order_by('-id')
    if user.is_authenticated:
        mypostings=Posting.objects.filter(landlord_id=user.id).all().order_by('-id')
        mycollections=Collection.objects.filter(User_id=user).all().order_by('-id')
    else:
        mypostings=None
        mycollections=None
    return render(request,'index.html',{"postings":postings,"mypostings":mypostings,"mycollection":mycollections})

#展示帖子的具体内容，评论等
def showPosting(request):
    no=request.GET['p']
    posting=Posting.objects.get(id=no)
    comments=Comment.objects.filter(c_Posting_id=posting).all().order_by('-c_Likes')
    return render(request,'posting.html',{"posting":posting,"comments":comments})

#重新加载展示帖子的网页
def reloadPosting(request,no):
    posting=Posting.objects.get(id=no)
    comments=Comment.objects.filter(c_Posting_id=posting).all()
    return render(request,'posting.html',{"posting":posting,"comments":comments})

#为评论点赞
def like(request):
    no=request.GET['c']
    comment=Comment.objects.get(id=no)
    user=request.user
    likes=comment.c_Likes
    if Like.objects.filter(User_id=user,Comment_id=comment):
        Like.objects.filter(User_id=user,Comment_id=comment).delete()
        Comment.objects.filter(id=no).update(c_Likes=likes-1)
    else:
        like=Like(User_id=user,Comment_id=comment)
        like.save()
        Comment.objects.filter(id=no).update(c_Likes=likes+1)
    p=comment.c_Posting_id
    return reloadPosting(request,p.id)

#评论帖子
def addComment(request):
    no=request.GET['p']
    posting=Posting.objects.get(id=no)
    content=request.GET['content']
    user=request.user
    date=timezone.localdate()
    comment=Comment(c_User_id=user,c_Content=content,c_Date=date,c_Posting_id=posting)
    comment.save()
    return reloadPosting(request,no)

#收藏帖子
def collect(request):
    user=request.user
    no=request.GET['p']
    posting=Posting.objects.get(id=no)
    if Collection(User_id=user,Posting_id=posting) is not None:
        collect=Collection(User_id=user,Posting_id=posting)
        collect.save()
    return reloadPosting(request,no)

#注册账号
def register(request):
    if request.method =='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmation=request.POST['confirmation']

        if not( username and email and password and confirmation ):
            return render(request,'register.html',{
                'message': "怎么什么都不输入，这可不行！"
            })
        if password==confirmation:
            try:
                user=User.objects.create_user(username,email,password)
                user.save()
            except IntegrityError:
                return render(request,'register.html',{
                    'message': "呜呜呜呜这个名字被人用啦！"
                })
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,'register.html',{
                "message" : "两次输入的密码不同哦~"
            })
    else:
        return render(request,'register.html')

#退出登录
@login_required
def logout_view(request):
    user=request.user
    user.is_online=0
    user.save()
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#游客浏览网站
def stroll(request):
    user=request.user
    if user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse("index"))

#登录
def log_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)

        if user is not None:
            auth_obj=authenticate(request,username=username,password=password,is_online=1)
            if auth_obj:
                auth.login(request,auth_obj)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,'login.html',{
                "message": "用户名或者密码错啦！"
            })
    else:
        return render(request,'login.html')

#展示个人信息
@login_required
def Showmyself(request):
    user=request.user
    return render(request,'myself.html',{
        "user" : user
    })

#修改个人信息
def modify(request):
    username=request.POST.get('uname')
    signature=request.POST.get('usig')
    user=request.user
    if username is not None:
        try:
            user.username=username
            user.save()
        except IntegrityError:
            return render(request,'myself.html',{
                'user' : user,
                'message': "呜呜呜这个名字有人用啦！"
            })
    if signature is not None:
        user.signature=signature
        user.save()
    return render(request,'myself.html',{
        "user" : user
    })

#上传头像
def changeHeadportrait(request):
    head=request.FILES.get('head')
    user=request.user
    user.headportrait=head
    user.save()
    return render(request,'myself.html',{
        "user" : user
    })   

#将帖子设置为仅自己可见
def icansee(request):
    no=request.GET['p']
    Posting.objects.filter(id=no).update(p_See=False)
    return reloadPosting(request,no)

#写帖子
def addPosting(request):
    if request.method == 'POST':
        user = request.user
        title=request.POST['t']
        content = request.POST['c']
        date=timezone.localdate()
        posting=Posting(landlord_id=user,p_Title=title,p_Des=content,p_Date=date)
        posting.save()
        return render(request, "posting.html",{"posting":posting})
    else:
        return render(request,'addposting.html')

#进入管理界面，可以管理帖子
def manage(request):
    postings=Posting.objects.all().order_by('-id')
    return render(request,'ManagePosting.html',{"postings":postings})

#删除帖子
def deletePosting(request):
    no=request.GET['p']
    Posting.objects.filter(id=no).delete()
    return manage(request)

#进入管理帖子的评论的界面，可以删除评论
def manageComment(request):
    no=request.GET['p']
    posting=Posting.objects.get(id=no)
    comments=Comment.objects.filter(c_Posting_id=posting).all().order_by('-id')
    return render(request,'ManageComment.html',{"comments":comments})

#重新加载管理评论的界面
def reloadManage(request,posting):
    comments=Comment.objects.filter(c_Posting_id=posting).all()
    return render(request,'ManageComment.html',{"comments":comments})

#删除评论
def deleteComment(request):
    no=request.GET['c']
    comment=Comment.objects.get(id=no)
    p=comment.c_Posting_id
    Comment.objects.filter(id=no).delete()
    return reloadManage(request,p)


#私信
def chat(request):
    return render(request,"chat.html")