from django.urls import path
from . import views



urlpatterns = [
    path('', views.overview, name = 'overview'),
    path('create', views.create_post, name = 'create_post'),
    path('register', views.register_user, name='register_user' ),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout')
]