from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

import sys, os
import pandas as pd
import numpy as np

from mm.models import Population, Strain, Marker, MSTable
from mm.forms import PopulationForm

UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/upload_files/'

#--- Index ---
def index(request):
    return render(request, 'mm/index.html', {'active_navi' : 0})


#--- Population ---
def population_list(request):
    """ Show List """
    population_recs = Population.objects.all().order_by('id')
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
    import sqlite3

    population = get_object_or_404(Population, pk=population_id)

    if request.method == 'POST':
        filename = request.POST['filename']

        f_in = UPLOADE_DIR + filename
        df = pd.read_csv(f_in, sep='\t', header=0)

        N_strains = len(df.columns[2:])
        N_markers = len(df['MARKER'])

        dict_strains = {
            'name'       : list(df.columns[2:]),
            'population' : population.id,
            'source'     : np.zeros(N_strains).tolist(),
            'taxon'      : np.zeros(N_strains).tolist(),
            'description': np.zeros(N_strains).tolist(),
        }
        df_strains = pd.DataFrame(dict_strains, columns=['name', 'population', 'source', 'taxon', 'description'])

        # dataframe to sqlite3
        conn = sqlite3.connect("db.sqlite3")     # ここパス修正
        df_strains.to_sql('{table}'.format(table='Strains'), conn, if_exists='append')
        #return HttpResponse(df_strains)


#--- Strain ---
def strain_list(request):
    """ Show List """
    strain_recs = Strain.objects.all().order_by('id')
    return render(
        request,
        'mm/strain_list.html',
        {'strain_recs': strain_recs, 'active_navi' : 2}
    )
