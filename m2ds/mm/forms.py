from django.forms import ModelForm, Form
from django import forms
from mm.models import Population

class PopulationForm(ModelForm):
    """Form for Population"""
    class Meta:
        model = Population
        fields = ('name', 'year', 'place', 'cultivator', 'description',)
