from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/<int:pk>/', views.community_detail, name='community_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]