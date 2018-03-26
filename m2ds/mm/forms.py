from django.forms import ModelForm
from mm.models import Cultivation

class CultivationForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Cultivation
        fields = ('name', 'year', 'place', 'cultivator', 'description',)
