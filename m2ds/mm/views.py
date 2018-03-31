# default library of django
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

# additional library for django
from django_pandas.io import read_frame

# default library of python
import sys, os, io
import pandas as pd
import numpy as np
import itertools
import urllib

# original library for M2DS
from mm.models import Population, Strain, Marker, MSTable
from mm.forms import PopulationForm, StrainForm, MarkerForm, MSTableForm

# IO directory
UPLOADE_DIR  = os.path.dirname(os.path.abspath(__file__)) + '/static/upload_files/'
DOWNLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/download_files/'

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


#--- Strain ---
def strain_list(request, population_id=None):
    population = Population.objects.all().order_by('name')

    if request.method == 'GET' and request.GET.get('population_id', None):
        population_id = request.GET.get('population_id', None)

    """ Show List """
    if population_id:
        strain_recs = Strain.objects.filter(population=population_id).order_by('population', 'name',)
        population_name = get_object_or_404(Population, pk=population_id).name

        return render(
            request,
            'mm/strain_list.html',
            {'strain_recs': strain_recs, 'population_name': population_name, 'population':population, 'active_navi' : 2}
        )

    else:
        strain_recs = Strain.objects.all().order_by('population', 'name',)

        return render(
            request,
            'mm/strain_list.html',
            {'strain_recs': strain_recs, 'population':population, 'active_navi' : 2}
        )


def strain_edit(request, strain_id):
    """ Edit """
    if strain_id:
        strain = get_object_or_404(Strain, pk=strain_id)
    else:
        return redirect('mm:strain_list')

    if request.method == 'POST':
        form = StrainForm(request.POST, instance=strain)
        if form.is_valid():
            strain = form.save(commit=False)
            strain.save()
            return redirect('mm:strain_list')
    else:
        ### When request is "GET"
        form = StrainForm(instance=strain)

    return render(
        request,
        'mm/strain_edit.html',
        {'form' : form, 'strain_id' : strain_id, 'active_navi' : 2}
    )


def strain_confirm(request, strain_id):
    """ Confirm """
    strain = get_object_or_404(Strain, pk=strain_id)
    return render(
        request,
        'mm/strain_confirm.html',
        {'strain' : strain, 'strain_id' : strain_id, 'active_navi' : 2}
    )


def strain_del(request, strain_id):
    """ Delete """
    strain = get_object_or_404(Strain, pk=strain_id)
    strain.delete()
    return redirect('mm:strain_list')



#--- Marker ---
def marker_list(request, population_id=None):
    """ Show List """
    population = Population.objects.all().order_by('name')

    if request.method == 'GET' and request.GET.get('population_id', None):
        population_id = request.GET.get('population_id', None)

    if population_id:
        genotype_marker_recs = Marker.objects.filter(population=population_id, mtype='g').order_by('population', 'name',)
        phenotype_marker_recs = Marker.objects.filter(population=population_id, mtype='p').order_by('population', 'name',)
        population_name = get_object_or_404(Population, pk=population_id).name

        return render(
            request,
            'mm/marker_list.html',
            {
                'genotype_marker_recs': genotype_marker_recs,
                'phenotype_marker_recs': phenotype_marker_recs,
                'population_name': population_name,
                'population':population,
                'active_navi' : 3,
            }
        )

    else:
        genotype_marker_recs = Marker.objects.filter(mtype='g').order_by('population', 'name',)
        phenotype_marker_recs = Marker.objects.filter(mtype='p').order_by('population', 'name',)

        return render(
            request,
            'mm/marker_list.html',
            {
                'genotype_marker_recs': genotype_marker_recs,
                'phenotype_marker_recs': phenotype_marker_recs,
                'population':population,
                'active_navi' : 3,
            }
        )


def marker_edit(request, marker_id):
    """ Edit """
    if marker_id:
        marker = get_object_or_404(Marker, pk=marker_id)
    else:
        return redirect('mm:marker_list')

    if request.method == 'POST':
        form = MarkerForm(request.POST, instance=marker)
        if form.is_valid():
            marker = form.save(commit=False)
            marker.save()
            return redirect('mm:marker_list')
    else:
        ### When request is "GET"
        form = MarkerForm(instance=marker)

    return render(
        request,
        'mm/marker_edit.html',
        {'form' : form, 'marker_id' : marker_id, 'active_navi' : 3}
    )


def marker_confirm(request, marker_id):
    """ Confirm """
    marker = get_object_or_404(Marker, pk=marker_id)
    return render(
        request,
        'mm/marker_confirm.html',
        {'marker' : marker, 'marker_id' : marker_id, 'active_navi' : 3}
    )


def marker_del(request, marker_id):
    """ Delete """
    marker = get_object_or_404(Marker, pk=marker_id)
    marker.delete()
    return redirect('mm:marker_list')


#--- MS Table ---
def make_pivot_table(population_id, outfmt='html'):
    ms_recs = MSTable.objects.filter(strain__population__id=population_id, marker__population__id=population_id)
    df = read_frame(ms_recs)
    pivot_table = df.pivot(index='marker', columns='strain', values='value').fillna('-')
    if outfmt=='html':
        pivot_dataset = pivot_table.to_html(index=True, classes=["table", "table-bordered", "table-sm", "table-hover"], col_space=200, na_rep='-')

    return pivot_dataset


def mstable_list(request, population_id=None):
    population = Population.objects.all().order_by('name')

    if request.method == 'GET' and request.GET.get('population_id', None):
        population_id = request.GET.get('population_id', None)

    """ Show List """
    if population_id:
        table_pop = get_object_or_404(Population, pk=population_id)
        strain_recs = Strain.objects.filter(population__id=population_id)
        marker_recs = Marker.objects.filter(population__id=population_id)
        pivot_html = make_pivot_table(population_id)
        return render(
            request,
            'mm/mstable_list.html',
            {
                'pivot_html': pivot_html,
                'table_pop': table_pop,
                'population' : population,
                'active_navi' : 4,
                'strain_recs' : strain_recs,
                'marker_recs' : marker_recs,
            }
        )

    else:
        return render(
            request,
            'mm/mstable_list.html',
            {'population' : population, 'active_navi' : 4}
        )


def mstable_view(request, strain_id=None, marker_id=None, population_id=None):
    if request.method == 'GET':
        population_id = request.GET.get('population_id', None)
        strain_id = request.GET.get('strain_id', None)
        marker_id = request.GET.get('marker_id', None)
    else:
        return redirect('mm:mstable_list')

    if not population_id:
        return redirect('mm:mstable_list')

    population = Population.objects.all().order_by('name')
    table_pop  = get_object_or_404(Population, pk=population_id)

    if strain_id and marker_id:
        recs = MSTable.objects.filter(marker__id=marker_id, strain__id=strain_id).order_by('marker', 'strain')
    elif strain_id:
        recs = MSTable.objects.filter(strain__id=strain_id).order_by('strain')
    elif marker_id:
        recs = MSTable.objects.filter(marker__id=marker_id).order_by('marker')
    else:
        strain_recs = Strain.objects.filter(population__id=population_id)
        marker_recs = Marker.objects.filter(population__id=population_id)
        pivot_html = make_pivot_table(population_id)
        return render(
            request,
            'mm/mstable_list.html',
            {
                'pivot_html'  : pivot_html,
                'population'  : population,
                'table_pop'   : table_pop,
                'strain_recs' : strain_recs,
                'marker_recs' : marker_recs,
                'active_navi' : 4,
            }
        )
    #return HttpResponse(marker_id)
    return render(
        request,
        'mm/mstable_view.html',
        {
            'recs' : recs,
            'table_pop_id': population_id,
            'strain_id'   : strain_id,
            'marker_id'   : marker_id,
            'active_navi' : 4,
        }
    )


def mstable_edit(request, mstable_id,):
    """ Edit """
    if mstable_id:
        mstable = get_object_or_404(MSTable, pk=mstable_id)
    else:
        return redirect('mm:mstable_list')

    if request.method == 'POST':
        form = MSTableForm(request.POST, instance=mstable)
        if form.is_valid():
            mstable = form.save(commit=False)
            mstable.save()
            return redirect('mm:mstable_list')

    else:
        ### When request is "GET"
        form = MSTableForm(instance=mstable)

    return render(
        request,
        'mm/mstable_edit.html',
        {
            'form' : form,
            'mstable_id' : mstable_id,
            'active_navi' : 4
        }
    )



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
        df = pd.read_csv(f_in, sep='\t', header=0).fillna('-')
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


def dataset_export(request, population_id, filename=None, sep='\t', extention='txt'):
    from django.urls import reverse

    if request.method == 'POST':

        if request.POST.get('filename', None):

            filename  = request.POST.get('filename', None)
            extention = request.POST.get('extention', None)
            filename_with_extention = filename + '.' + extention
            outfile = DOWNLOAD_DIR + filename_with_extention

            # Get sql-query
            ms_recs = MSTable.objects.filter(strain__population__id=population_id, marker__population__id=population_id)
            mk_recs = Marker.objects.filter(population__id=population_id).values('name', 'mtype')

            # sql-query to dataframe
            df = read_frame(ms_recs)
            mk = read_frame(mk_recs)

            # dataframe to pivot
            pivot_df = df.pivot(index='marker', columns='strain', values='value').fillna('-')

            # modify
            pivot_df = pivot_df.merge(mk, left_index=True, right_on='name', how='left')
            cols = list(pivot_df.columns[-2:]) + list(pivot_df.columns[:-2])
            pivot_df = pivot_df.loc[:,cols]
            pivot_df = pivot_df.rename(columns={'name': 'MARKER', 'mtype': 'TYPE'})
            # pivot_df.columns[0] = pivot_df.columns[0].str.replace('name', 'marker').str.upper()
            # pivot_df.columns[1] = pivot_df.columns[1].str.replace('mtype', 'type').str.upper()
            pivot_df['TYPE'] = pivot_df['TYPE'].replace('Phenotype', 'p')
            pivot_df['TYPE'] = pivot_df['TYPE'].replace('Genotype', 'g')

            # output
            pivot_df.to_csv(outfile, sep=sep, index=False, header=True)

            # download
            response = HttpResponse(open(outfile,'rb').read(), content_type="text/plain")
            response["Content-Disposition"] = "attachment; filename=%s" % filename_with_extention

            return response
            #return redirect('mm:population_list')

        else:
            if request.POST.get('population_id', None):
                population_id = request.POST.get('population_id', None)
            population = get_object_or_404(Population, pk=population_id)

            return render(
                request,
                'mm/dataset_download.html',
                {'population' : population, 'active_navi' : 1,}
            )

    else:
        ### When request is "GET"
        if request.GET.get('population_id', None):
            population_id = request.GET.get('population_id', None)
        population = get_object_or_404(Population, pk=population_id)

        return render(
            request,
            'mm/dataset_download.html',
            {'population' : population, 'active_navi' : 1,}
        )
