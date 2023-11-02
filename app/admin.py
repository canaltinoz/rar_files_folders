from django.contrib import admin
from .models import *

@admin.register(CompressedFile)
class CompressedFileAdmin(admin.ModelAdmin):
    list_display = ('compressed_file','password')  
