from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.say_hello, name='index'),
    path("", views.welcome,),
    path('login/', views.login),
    path('signup/', views.signup),
    path('post/', views.makepost)
]

