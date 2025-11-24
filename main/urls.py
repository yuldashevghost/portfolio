from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('skills/<int:pk>/edit/', views.skill_update, name='skill_update'),
    path('projects/add/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('gallery/add/', views.gallery_create, name='gallery_create'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
    path('blog/add/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('contact-messages/', views.contact_messages, name='contact_messages'),
]


