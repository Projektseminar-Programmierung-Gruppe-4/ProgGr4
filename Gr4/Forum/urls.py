from django.conf.urls import url
from django.urls import path
from . import views



urlpatterns = [
    path('', views.overview, name = 'overview'),
    path('create', views.create_post, name = 'create_post'),
    path('register', views.register_user, name='register_user' ),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('post/<pk>', views.detail, name='detail'),
    path('post/<pk>/update', views.update_post, name='update'),
    path('post/<pk>/delete', views.delete_post, name='delete'),
    path('post/<pk>/<vote>', views.vote_post, name='vote-post'),
    path('comment/<pk>/update', views.update_comment, name='update-comment'),
    path('comment/<pk>/delete', views.delete_comment, name='delete-comment'),
    path('comment/<pk>/<vote>', views.vote_comment, name='vote-comment')
]