from django.contrib import admin
from django.urls import path, include
import images
from . import views
urlpatterns = [
    path('', views.index),
    # path('image/<int:pk>', views.image_detail)
]
