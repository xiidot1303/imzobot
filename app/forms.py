from django.forms import ModelForm, widgets
from app.models import *
from django import forms


class UploadFileFrom(forms.Form):
    file = forms.FileField(allow_empty_file=False, required=True, label='Файл', widget = forms.FileInput(attrs={'class': 'form-control'}))
    lang = forms.CharField(widget=forms.Select(choices=[('uz', 'uz'), ('ru', 'ru')], attrs={'class': 'form-control'}))
