from django.urls import  path
from . import views

urlpatterns=[
    path("",views.entry,name="entry"),
    path("index",views.index,name="index"),
    path("showposting",views.showPosting,name="showposting"),
    path("like",views.like,name="like"),
    path("collect",views.collect,name="collect"),
    path("comment",views.addComment,name="comment"),
    path("register",views.register,name='register'),
    path("login",views.log_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("myself",views.Showmyself,name='myself'),
    path("addposting",views.addPosting,name="addposting"),
    path("icansee",views.icansee,name="icansee"),
    path("manageposting",views.managePosting,name="managepodting"),
    path("deleteposting",views.deletePosting,name="deleteposting"),
    path("managecomment",views.manageComment,name="managecomment"),
    path("deletecomment",views.deleteComment,name="deletecomment")
]