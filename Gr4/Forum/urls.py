from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
    path('', views.overview, name = 'overview'),
    path('create', views.create_post, name = 'create_post'),
    path('register', views.register_user, name='register_user' ),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    #url('^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    path('post/<pk>', views.detail, name='detail'),
    #path('post/<pk>/update', views.PostUpdateView.as_view(), name='update'),
    path('post/<pk>/update', views.update_post, name='update'),
    path('post/<pk>/delete', views.delete_post, name='delete'),
    path('comment/<pk>/update', views.update_comment, name='update-comment'),
    path('comment/<pk>/delete', views.delete_comment, name='delete-comment'),
    path('comment/<pk>/like', views.like_comment, name='like-comment'),
    path('comment/<pk>/dislike', views.dislike_comment, name='dislike-comment')
]