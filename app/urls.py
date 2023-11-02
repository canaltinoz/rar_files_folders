from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('upload-folder/', views.upload_files, name='upload_files'),
    path('files/', views.file_list, name='file_list'),
]