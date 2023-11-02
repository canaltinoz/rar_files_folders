from django.db import models

class CompressedFile(models.Model):
    compressed_file = models.FileField(upload_to='compressed_files/')
    password = models.CharField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class CompressedFolder(models.Model):
    compressed_folder = models.FileField(upload_to='compressed_folders/')
    password = models.CharField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

