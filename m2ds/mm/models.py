from django.db import models
from django.core.validators import RegexValidator


class Population(models.Model):
    year_number_regex = RegexValidator(regex=r'^[0-9]{0,4}$', message='Year number')

    id     = models.AutoField('ID', primary_key=True)
    name   = models.CharField('Name', max_length=50)
    year   = models.IntegerField('Year', validators=[year_number_regex])
    place  = models.CharField('Place', max_length=50, blank=True)
    cultivator  = models.CharField('Cultivator', max_length=20, blank=True)
    description = models.TextField('Description', blank=True)

    class Meta:
        unique_together = ('name', 'year')

    def __str__(self):
        return self.name


class Strain(models.Model):
    id     = models.AutoField('ID', primary_key=True)
    name   = models.CharField('Name', max_length=20)
    population = models.ForeignKey(Population, to_field='id', related_name='strains', on_delete=models.CASCADE)
    source = models.ManyToManyField("self", related_name='Strain_ID', verbose_name="pre-generation", blank=True)
    taxon  = models.CharField('Taxon', max_length=50, blank=True)
    description = models.TextField('Description', blank=True)

    class Meta:
        unique_together = ('name', 'population')

    def __str__(self):
        return self.name


class Marker(models.Model):
    marker_types = (('g', 'Genetic Marker'), ('p', 'Phenotypic Marker'))

    id     = models.AutoField('ID', primary_key=True)
    name   = models.CharField('Name', max_length=20)
    population = models.ForeignKey(Population, to_field='id', related_name='markers', on_delete=models.CASCADE)
    mtype  = models.CharField('Type', max_length=20, choices=marker_types, default='g', blank=False)
    description = models.TextField('Description', blank=True)

    class Meta:
        unique_together = ('name', 'population')

    def __str__(self):
        return self.name


class MSTable(models.Model):
    id     = models.AutoField('ID', primary_key=True)
    strain = models.ForeignKey(Strain, to_field='id', related_name='strains', on_delete=models.CASCADE)
    marker = models.ForeignKey(Marker, to_field='id', related_name='markers', on_delete=models.CASCADE)
    value  = models.CharField('Value', max_length=10, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)

    class Meta:
        unique_together = ('strain', 'marker')

    def __str__(self):
        return str(self.id)
