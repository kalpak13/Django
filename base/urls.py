from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('login/',views.login_page,name='login'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('',views.Home,name='home'),
    path('room/<str:pk>/',views.Room,name='room'),
    path('create-room/',views.create_room,name='create-room'),
    path('update-room/<str:pk>',views.update_room,name='update-room'),
    path('delete-room/<str:pk>',views.delete_room,name='delete-room'),
    path('delete-messgae/<str:pk>',views.delete_comment,name='delete-comment'),



]