from django.urls import path
from . import views



urlpatterns = [
    path('', views.overview, name = 'overview'),
    path('create', views.create_post, name = 'create_post')
]