from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from mm.models import Cultivation, Strain, Marker, Management
from mm.forms import CultivationForm

#--- Cultivation ---
def cult_list(request):
    """ Show List """
    cult_recs = Cultivation.objects.all().order_by('id')
    return render(request, 'mm/cult_list.html', {'cult_recs': cult_recs})


def cult_edit(request, cult_id=None):
    """ Edit """
    if cult_id:
        cultivation = get_object_or_404(Cultivation, pk=cult_id)
    else:
        cultivation = Cultivation()

    if request.method == 'POST':
        form = CultivationForm(request.POST, instance=cultivation)
        if form.is_valid():
            cultivation = form.save(commit=False)
            cultivation.save()
            return redirect('mm:cult_list')
    else:
        ### When request is "GET"
        form = CultivationForm(instance=cultivation)

    return render(request, 'mm/cult_edit.html', dict(form=form, cult_id=cult_id))

def cult_del(request, cult_id):
    """ Delete """
    cultivation = get_object_or_404(Cultivation, pk=cult_id)
    cultivation.delete()
    return redirect('mm:cult_list')


#--- Strain ---
def strain_list(request):
    """ Show List """
    strain_recs = Strain.objects.all().order_by('id')
    return render(request, 'mm/strain_list.html', {'strain_recs': strain_recs})
