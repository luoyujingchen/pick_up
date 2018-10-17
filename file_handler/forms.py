from django import forms
from django.forms import ModelForm

from file_handler.models import Img


class UploadFileForm(ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = Img
        exclude = ['id']