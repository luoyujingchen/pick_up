from django import forms
from django.forms import ModelForm

from file_handler.models import Img


class UploadFileForm(ModelForm):
    class Meta:
        model = Img
        exclude = ['id']