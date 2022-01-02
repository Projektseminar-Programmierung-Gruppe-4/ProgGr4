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
    path('comment/<pk>/<vote>', views.vote_comment, name='vote-comment'),
    path('archiv', views.archiv, name = 'archiv'),
    path('post/<pk>/report/', views.report_post, name = 'report-post'),
    path('comment/<pk>/report/', views.report_comment, name = 'report-comment'),
    path('reports', views.reports, name='reports'),
    path('reports/<pk>/<type>/release/', views.release_report, name='release-report'),
    path('reports/<pk>/<type>/delete/', views.delete_report, name='delete-report'),
    path('adminpage', views.adminpage, name='adminpage'),
    path('departments', views.add_department, name='departments'),
    path('departments/<pk>/delete/', views.delete_department, name='delete-department'),
    path('permissions', views.permission_overview, name='permissions'),
    path('permissions/<pk>/set', views.set_permission, name='set-permission'),
    path('permissions/<pk>/remove', views.remove_permission, name='remove-permission')
]