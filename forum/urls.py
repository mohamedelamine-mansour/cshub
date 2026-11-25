from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/<int:pk>/', views.community_detail, name='community_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('post/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('search/', views.search, name='search'),
    path('post/<int:pk>/report/', views.report_create, name='report_create'),
]