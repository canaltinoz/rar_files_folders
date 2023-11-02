from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import CompressedFile
import zipfile,subprocess,rarfile,patoolib,shutil,tempfile,pyzipper
import os
from django.db import transaction
from django.core.files import File
import pandas as pd

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
            compressed_file.password = password
            compressed_file.save() 

            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)

                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                if uploaded_file.name.endswith('.csv'):
                    csv_data = pd.read_csv(file_path,encoding='latin1')
                    xlsx_path = os.path.splitext(file_path)[0] + '.xlsx'
                    csv_data.to_excel(xlsx_path, index=False,header=True)
                    os.remove(file_path)
                
                else:
                    final_file_path = os.path.join(temp_dir, uploaded_file.name)
                    os.rename(file_path, final_file_path)


                
            zip_file_path = os.path.join(temp_dir, f'compressed_files_{compressed_file.id}.zip')
            os.chdir(temp_dir)
            patoolib.create_archive(zip_file_path, ('.',), password=password)
            os.chdir(os.path.dirname(zip_file_path))

            with open(zip_file_path, 'rb') as zip_file:
                compressed_file.compressed_file.save(f'compressed_files_{compressed_file.id}.zip', File(zip_file))
                compressed_file.save()

            return redirect(file_list)
        except:
            return redirect(file_list)
            
    return render(request, 'upload_files.html')
##################################################################################

def upload_folder(request):
    if request.method == 'POST':
        uploaded_folder = request.FILES.getlist('folderInput')
        password = request.POST.get('password')  
        temp_dir = tempfile.mkdtemp()

        try:
            compressed_folder = CompressedFolder()
            compressed_folder.password = password
            compressed_folder.save()

            for folder in uploaded_folder:
                file_path = os.path.join(temp_dir, folder.name)
                with open(file_path, 'wb') as destination:
                    for chunk in folder.chunks():
                        destination.write(chunk)

            zip_file_path = os.path.join(temp_dir, f'compressed_folder_{compressed_folder.id}.zip')
            os.chdir(temp_dir)
            patoolib.create_archive(zip_file_path, ('.',), password=password)
            os.chdir(os.path.dirname(zip_file_path))

            with open(zip_file_path, 'rb') as zip_file:   
                compressed_folder.compressed_folder.save(f'compressed_folder_{compressed_folder.id}.zip', File(zip_file))
                compressed_folder.save()
            return redirect(folder_list)
        
        except:
            return redirect(folder_list)
    return render(request, 'upload_folder.html')

#############################################################################################

def file_list(request):
    files = CompressedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})

def folder_list(request):
    folders = CompressedFolder.objects.all()
    return render(request, 'folder_list.html', {'folders': folders})


