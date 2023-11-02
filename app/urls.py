from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('upload-files/', views.upload_files, name='upload_files'),
    path('upload-folder/', views.upload_folder, name='upload_folder'),
    path('files/', views.file_list, name='file_list'),
    path('folders/', views.folder_list, name='folder_list'),

]