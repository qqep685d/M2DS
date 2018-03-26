from django.contrib import admin
from mm.models import Cultivation, Strain, Marker, Management


#--- Cultivation ---
class CultivationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'place', 'cultivator',)  # Display
    list_display_links = ('id', 'name',)  # Link
admin.site.register(Cultivation, CultivationAdmin)


#--- Strain ---
class StrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'population', 'taxon',)  # Display
    list_display_links = ('id', 'name',)  # Link
admin.site.register(Strain, StrainAdmin)


#--- Marker ---
admin.site.register(Marker)


#--- Management ---
admin.site.register(Management)
