from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/done/', views.register_done, name='register_done'),
]