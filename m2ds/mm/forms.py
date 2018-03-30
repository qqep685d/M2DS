from django.forms import ModelForm, Form, modelformset_factory
from django import forms
from mm.models import Population, Strain, Marker, MSTable

class PopulationForm(ModelForm):
    """Form for Population"""
    class Meta:
        model = Population
        fields = ('name', 'year', 'place', 'cultivator', 'description',)


class StrainForm(ModelForm):
    """Form for Strain"""
    class Meta:
        model = Strain
        fields = ('name', 'taxon', 'description',)


class MarkerForm(ModelForm):
    """Form for Strain"""
    class Meta:
        model = Marker
        fields = ('name', 'mtype', 'description',)


class MSTableForm(ModelForm):
    """Form for MSTable"""
    class Meta:
        model = MSTable
        fields = ('value', 'description',)
