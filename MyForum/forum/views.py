from audioop import reverse
from sys import float_repr_style
from django.db import IntegrityError
from django.shortcuts import render

from .models import Collection, User, Posting, Comment
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# Create your views here.

def entry(request):
    return render(request,'entry.html')

def index(request):
    user=request.user
    postings=Posting.objects.all()
    mypostings=Posting.objects.filter(p_User=user).all()
    return render(request,'index.html',{postings:postings , mypostings:mypostings})

def showPosting(request):
    no=request.GET['p']
    posting=Posting.objects.get(id=posting.id)
    comments=Comment.objects.filter(c_Posting=posting).all()
    return render(request,'posting.html',{posting:posting,comments:comments})

def like(request):
    no=request.GET['p']
    likes=Posting.objects.filter(id=posting.id).values('p_Likes')
    posting=Posting.objects.filter(id=posting.id).update(p_Likes=likes+1)

def addComment(request):
    no=request.GET['p']
    content=request.GET['content']
    user=request.user
    date=timezone.localdate()
    comment=Comment(c_User_id=user,c_Content=content,c_Date=date)
    comment.save()
    return True

def collect(request):
    user=request.user
    p=request.GET['p']
    posting=Posting.objects.get(id=p)
    if(Collection.objects.filter(User_id=user,Posting_id=posting) == None):
        collect=Collection(User_id=user,Posting_id=posting)
        collect.save()
        return True
    else : 
        return False

def register(request):
    if request.method =='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmation=request.POST['confirmation']

        if password==confirmation:
            try:
                user=User.objects.create_uaer(username,email,password)
                user.save()
            except IntegrityError:
                return render(request,'register.html',{
                    'message': "Username already taken."
                })
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'register.html',{
                "message" : "Password doesn't match the confirmation."
            })
    else:
        return render(request,'register.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def log_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)

        if user is not None:
            auth_obj=authenticate(request,username=username,password=password)
            if auth_obj:
                auth.login(request,auth_obj)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'login.html',{
                "message": "Invalid username or password."
            })
    else:
        return render(request,'login.html')

@login_required
def Showmyself(request):
    if request.meyhod=='POST':
        username=request.POST['username']
        signature=request.POST['signature']
        img=request.POST['img']
        user=request.user
        if username!='':
            try:
                user.username=username
                user.save()
            except IntegrityError:
                return render(request,'myself.html',{
                    'user' : user,
                    'message': "Username already taken."
                })
        if signature!='':
            user.signature=signature
            user.save()
        if img!='':
            user.headportrait=img
            user.save()
        return render(request,'myself.html',{
            "user" : user
        })
    user=request.user
    return render(request,'myself.html',{
        "user" : user
    })