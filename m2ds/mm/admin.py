from django.contrib import admin
from mm.models import Population, Strain, Marker, MSTable


#--- Cultivation ---
class PopulationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'place', 'cultivator',)  # Display
    list_display_links = ('id', 'name',)  # Link
admin.site.register(Population, PopulationAdmin)


#--- Strain ---
class StrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'population', 'taxon',)  # Display
    list_display_links = ('id', 'name',)  # Link
admin.site.register(Strain, StrainAdmin)


#--- Marker ---
class MarkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'population', 'mtype',)  # Display
    list_display_links = ('id', 'name',)  # Link
admin.site.register(Marker, MarkerAdmin)


#--- Management ---
class MSTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'strain', 'marker', 'value',)  # Display
    list_display_links = ('id', 'strain', 'marker',)  # Link
admin.site.register(MSTable, MSTableAdmin)
