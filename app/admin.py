from django.contrib import admin
from .models import *

@admin.register(CompressedFile)
class CompressedFileAdmin(admin.ModelAdmin):
    list_display = ('uploaded_file','compressed_file','password')  

@admin.register(CompressedFolder)
class CompressedFileAdmin(admin.ModelAdmin):
    list_display = ('uploaded_folder','compressed_folder','password')  