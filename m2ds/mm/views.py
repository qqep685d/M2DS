from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

import sys, os
import pandas as pd
import numpy as np
import itertools
from django_pandas.io import read_frame

from mm.models import Population, Strain, Marker, MSTable
from mm.forms import PopulationForm

UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/upload_files/'

#--- Index ---
def index(request):
    return render(request, 'mm/index.html', {'active_navi' : 0})


#--- Population ---
def population_list(request):
    """ Show List """
    population_recs = Population.objects.all().order_by('-year', 'name', 'id')
    return render(
        request,
        'mm/population_list.html',
        {'population_recs' : population_recs, 'active_navi' : 1}
    )


def population_edit(request, population_id=None):
    """ Edit """
    if population_id:
        population = get_object_or_404(Population, pk=population_id)
    else:
        population = Population()

    if request.method == 'POST':
        form = PopulationForm(request.POST, instance=population)
        if form.is_valid():
            population = form.save(commit=False)
            population.save()
            return redirect('mm:population_list')
    else:
        ### When request is "GET"
        form = PopulationForm(instance=population)

    return render(
        request,
        'mm/population_edit.html',
        {'form' : form, 'population_id' : population_id, 'active_navi' : 1}
    )


def population_confirm(request, population_id):
    """ Confirm """
    population = get_object_or_404(Population, pk=population_id)
    return render(
        request,
        'mm/population_confirm.html',
        {'population' : population, 'population_id' : population_id, 'active_navi' : 1}
    )


def population_del(request, population_id):
    """ Delete """
    population = get_object_or_404(Population, pk=population_id)
    population.delete()
    return redirect('mm:population_list')


#--- Dataset ---
def dataset_upload(request, population_id):
    """ Upload Dataset """
    population = get_object_or_404(Population, pk=population_id)

    if request.FILES:
        upload_file = request.FILES['file']
        path = os.path.join(UPLOADE_DIR, upload_file.name)
        destination = open(path, 'wb')

        for chunk in upload_file.chunks():
            destination.write(chunk)

        return render(
            request,
            'mm/dataset_upload.html',
            {'population' : population, 'uploaded_file' : upload_file.name, 'active_navi' : 1}
        )

    else:
        return render(
            request,
            'mm/dataset_upload.html',
            {'population' : population, 'active_navi' : 1}
        )


def dataset_import(request, population_id):

    population = get_object_or_404(Population, pk=population_id)

    if request.method == 'POST':
        filename = request.POST['filename']

        # dataset into pandas-dataframe
        f_in = UPLOADE_DIR + filename
        df = pd.read_csv(f_in, sep='\t', header=0)
        strain_names  = list(df.columns[2:])
        marker_names  = list(df['MARKER'])
        marker_mtypes = list(df['TYPE'])

        # update or insert data from pandas-dataframe
        for n in strain_names:
            Strain.objects.update_or_create(name=n, population=Population(id=population.id))
        for n, t in zip(marker_names, marker_mtypes):
            Marker.objects.update_or_create(name=n, population=Population(id=population.id), defaults={'mtype':t})

        ms_comb = itertools.product(strain_names, marker_names)
        for c in ms_comb:
            get_strain = Strain.objects.get(name=c[0], population=population.id)
            get_marker = Marker.objects.get(name=c[1], population=population.id)
            m = marker_names.index(get_marker.name)
            s = get_strain.name
            val = df.loc[m, s]
            MSTable.objects.update_or_create(strain=Strain(id=get_strain.id), marker=Marker(id=get_marker.id), defaults={'value':val})

        return redirect('mm:population_list')


#--- Strain ---
def strain_list(request, population_id=None):
    """ Show List """
    if population_id:
        strain_recs = Strain.objects.filter(population=population_id).order_by('population', 'name',)
        population_name = get_object_or_404(Population, pk=population_id).name

        return render(
            request,
            'mm/strain_list.html',
            {'strain_recs': strain_recs, 'population_name': population_name, 'active_navi' : 2}
        )

    else:
        strain_recs = Strain.objects.all().order_by('population', 'name',)

        return render(
            request,
            'mm/strain_list.html',
            {'strain_recs': strain_recs, 'active_navi' : 2}
        )


#--- Marker ---
def marker_list(request, population_id=None):
    """ Show List """
    if population_id:
        genotype_marker_recs = Marker.objects.filter(population=population_id, mtype='g').order_by('population', 'name',)
        phenotype_marker_recs = Marker.objects.filter(population=population_id, mtype='p').order_by('population', 'name',)
        population_name = get_object_or_404(Population, pk=population_id).name

        return render(
            request,
            'mm/marker_list.html',
            {'genotype_marker_recs': genotype_marker_recs, 'phenotype_marker_recs': phenotype_marker_recs, 'population_name': population_name, 'active_navi' : 3}
        )

    else:
        genotype_marker_recs = Marker.objects.filter(mtype='g').order_by('population', 'name',)
        phenotype_marker_recs = Marker.objects.filter(mtype='p').order_by('population', 'name',)

        return render(
            request,
            'mm/marker_list.html',
            {'genotype_marker_recs': genotype_marker_recs, 'phenotype_marker_recs': phenotype_marker_recs, 'active_navi' : 3}
        )


#--- MS Table ---
def mstable_list(request, population_id=None):
    """ Show List """
    if population_id:
        population_name = get_object_or_404(Population, pk=population_id).name
        ms_recs = MSTable.objects.filter(strain__population__id=population_id, marker__population__id=population_id)
        df = read_frame(ms_recs)
        pivot_table = df.pivot(index='marker', columns='strain', values='value')
        pivot_html  = pivot_table.to_html(index=True, classes=["table-bordered", "table-striped"], col_space=200, na_rep='-')

        return render(
            request,
            'mm/mstable_list.html',
            {'pivot_html': pivot_html, 'population_name': population_name, 'active_navi' : 4}
        )
    else:
        return redirect('mm:population_list')
