from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import CompressedFile
import zipfile,subprocess,rarfile,patoolib,shutil,tempfile,pyzipper
import os

def index(request):
    return render(request,'index.html')

##################################################################################

def upload_files(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('posts')
        password = request.POST.get('password')  
        temp_dir = tempfile.mkdtemp()
        try:
            compressed_file = CompressedFile()
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
            zip_file_path = os.path.join(temp_dir, 'compressed_files.zip')
            patoolib.create_archive(zip_file_path, (temp_dir,), password=password)            
            compressed_file.compressed_file.save('compressed_files.zip', open(zip_file_path, 'rb'))
            compressed_file.password = password
            compressed_file.save()

            with open(zip_file_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename=compressed_files.zip'
                return redirect(file_list)
        finally:
            shutil.rmtree(temp_dir)
    return render(request, 'upload_files.html')
##################################################################################

def upload_folder(request):
    if request.method == 'POST':
        uploaded_folder = request.FILES.getlist('folderInput')
        password = request.POST.get('password')  
        temp_dir = tempfile.mkdtemp()

        try:
            compressed_folder = CompressedFolder()
            for folder in uploaded_folder:
                file_path = os.path.join(temp_dir, folder.name)
                with open(file_path, 'wb') as destination:
                    for chunk in folder.chunks():
                        destination.write(chunk)

            zip_file_path = os.path.join(temp_dir, 'compressed_folder.zip')
            patoolib.create_archive(zip_file_path, (temp_dir,), password=password)            
            compressed_folder.compressed_folder.save('compressed_folder.zip', open(zip_file_path, 'rb'))
            compressed_folder.password = password
            compressed_folder.save()

            with open(zip_file_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename=compressed_folder.zip'
                return redirect(folder_list)
        finally:
            shutil.rmtree(temp_dir)
        
    return render(request, 'upload_folder.html')

#############################################################################################

def file_list(request):
    files = CompressedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})

def folder_list(request):
    folders = CompressedFolder.objects.all()
    return render(request, 'folder_list.html', {'folders': folders})


