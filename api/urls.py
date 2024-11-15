from django.urls import path,include
from . import views
from djoser import views as djoser_views


urlpatterns = [
    path('djoser/', include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('authtoken/',include('djoser.urls.authtoken')),
    path('updateusername/<str:pk>',views.UpdateUser.as_view(),name='update'),
    path('getuserposts/<str:pk>',views.PostGetUser.as_view(),name='getuserposts'),
    path('createcomment',views.CreateComment.as_view(), name="createcomment"),
    path('getcommentonpost/<str:pk>', views.GetCommentThreads.as_view(),name='getcommentsthreads'),
    path('deletepost/<str:pk>',views.DeletePost.as_view(), name="deletepost"),
    path('updatepost/<str:pk>',views.UpdatePost.as_view(), name="updatepost"),
    path('searchuser/',views.SearchUser.as_view(), name='searchuser'),
    path('logout',views.UserLogout.as_view(),name='logout'),
    path('usersp',views.SpecificUserView.as_view(),name='user-view'),
    path('createpost',views.CreatePost.as_view(), name='createpost'),
    path('getpost',views.PostGet.as_view(),name='postget'),
    path('getmembers', views.GetMembers.as_view(),name='members'),
    path('createmembers',views.PostMember.as_view(),name='postmembers')
]