from django.db import models
from django.core.validators import RegexValidator

class Cultivation(models.Model):
    year_number_regex = RegexValidator(regex=r'^[1-2][0-9][0-9][0-9]$', message='YearNumber')

    id     = models.AutoField('ID', primary_key=True)
    name   = models.CharField('Name', max_length=50)
    year   = models.IntegerField('Year', validators=[year_number_regex])
    place  = models.CharField('Place', max_length=50, blank=True)
    cultivator  = models.CharField('Cultivator', max_length=20, blank=True)
    description = models.TextField('Description', blank=True)

class Strain(models.Model):
    id     = models.AutoField('ID', primary_key=True)
    name   = models.CharField('Name', max_length=20, unique=True)
    population = models.ForeignKey(Cultivation, to_field='id', blank=True, null=True, on_delete=models.SET_NULL, related_name='cultivation_id')
    source = models.ManyToManyField("self", verbose_name="pre-generation", blank=True, related_name='strain_id')
    taxon  = models.CharField('Taxon', max_length=50, blank=True)
    description = models.TextField('Description', blank=True)

class Marker(models.Model):
    marker_types = (('G', 'Genetic Marker'), ('T', 'Traits'))

    id     = models.AutoField('ID', primary_key=True)
    name   = models.CharField('Name', max_length=20, unique=True)
    mtype  = models.CharField('Type', max_length=20, choices=marker_types, default='G', blank=False)
    description = models.TextField('Description', blank=True)

class Management(models.Model):
    id     = models.AutoField('ID', primary_key=True)
    strain = models.ForeignKey(Strain, to_field='id', on_delete=models.CASCADE, related_name='strain_id')
    marker = models.ForeignKey(Marker, to_field='id', on_delete=models.CASCADE, related_name='marker_id')
    value  = models.CharField('Value', max_length=10, null=True, blank=True)
    description = models.TimeField('Description', blank=True)
