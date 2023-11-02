from django import forms
from .models import *

class UploadMultipleFilesForm(forms.Form):
    files = forms.FileField()
    password = forms.CharField(max_length=50, required=False)
