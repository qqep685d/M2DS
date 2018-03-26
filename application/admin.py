from django.contrib import admin
from .models import Cultivation, Strain, Marker, Management

admin.site.register(Cultivation)
admin.site.register(Strain)
admin.site.register(Marker)
admin.site.register(Management)
