from django.db import models

class CompressedFile(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
    compressed_file = models.FileField(upload_to='compressed/')
    password = models.CharField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class CompressedFolder(models.Model):
    uploaded_folder = models.FileField(upload_to='uploads/')
    compressed_folder = models.FileField(upload_to='compressed/')
    password = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

