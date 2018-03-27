from django.forms import ModelForm
from django import forms
from mm.models import Cultivation

class CultivationForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Cultivation
        fields = ('name', 'year', 'place', 'cultivator', 'description',)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
