from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('',views.Home,name='home'),
    path('room/<str:pk>/',views.Room,name='room'),


]