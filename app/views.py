from django.shortcuts import render, redirect
from .forms import *
from .models import CompressedFile
import zipfile,subprocess,rarfile,patoolib,shutil,tempfile
import os

def index(request):
    return render(request,'index.html')

################### FOR FILE #################################################
def compress_file(file_path, compressed_path, password):
    patoolib.create_archive(compressed_path, (file_path,), password=password)

def upload_and_compress(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            password = form.cleaned_data['password']

            file_name_without_extension, _ = os.path.splitext(os.path.basename(instance.uploaded_file.name))
            compressed_path = f'compressed/{file_name_without_extension}.zip'
            file_path = instance.uploaded_file.path

            compress_file(file_path, compressed_path, password)
            instance.compressed_file = compressed_path
            instance.save()
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_and_compress_file.html', {'form': form})

################### FOR FOLDER #################################################

##################################################################################

def file_list(request):
    files = CompressedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})
