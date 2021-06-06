from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('search/', search, name="search"),
    path('register/',register,name='register'),
    path('update/<int:id>',update_key,name='update'),
    path('delete/<int:id>',delete_key,name='delete'),
    path('myfile/<int:id>',myfiles,name='myfiles'),
    path('detail/<int:pk>',delete_key,name='detail'),
    path('login/',login,name='login'),
    path('logout/',logout_view,name='logout'),
    path('addkey/',addkey,name='key')
]
