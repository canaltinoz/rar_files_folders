from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('upload/', views.upload_and_compress, name='upload_and_compress'),
    path('files/', views.file_list, name='file_list'),
]