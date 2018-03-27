from django.forms import ModelForm, Form
from django import forms
from mm.models import Population

class PopulationForm(ModelForm):
    """Form for Population"""
    class Meta:
        model = Population
        fields = ('name', 'year', 'place', 'cultivator', 'description',)

class UploadFileForm(Form):
    """Form for File Uploader"""
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
