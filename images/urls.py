from django.contrib import admin
from django.urls import path, include
import images
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('image/<uuid:image_id>/', views.img_detail,name='detail')
]
