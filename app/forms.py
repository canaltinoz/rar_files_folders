from django import forms
from .models import *

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = CompressedFile
        fields = ('uploaded_file', 'password')

    password = forms.CharField(widget=forms.PasswordInput)


class UploadFolderForm(forms.ModelForm):
    class Meta:
        model = CompressedFolder
        fields = ('uploaded_folder', 'password')

    password = forms.CharField(widget=forms.PasswordInput)
    uploaded_folder = forms.FileField(widget=forms.ClearableFileInput(attrs={'webkitdirectory': True, 'directory': True}))
