from django.urls import  path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("",views.entry,name="entry"),
    path("index",views.index,name="index"),
    path("showposting",views.showPosting,name="showposting"),
    path("like",views.like,name="like"),
    path("collect",views.collect,name="collect"),
    path("addcomment",views.addComment,name="addcomment"),
    path("register",views.register,name='register'),
    path("login",views.log_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("myself",views.Showmyself,name='myself'),
    path("modify",views.modify,name="modify"),
    path("addposting",views.addPosting,name="addposting"),
    path("icansee",views.icansee,name="icansee"),
    path("manage",views.manage,name="manage"),
    path("deleteposting",views.deletePosting,name="deleteposting"),
    path("managecomment",views.manageComment,name="managecomment"),
    path("deletecomment",views.deleteComment,name="deletecomment")
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)