from django.forms import ModelForm
from .models import Familia


class FamiliaForm(ModelForm):
    class Meta:
        model = Familia
        fields = ('numero_hijos_diferentes_papas',
                  'estado_civil',
                  'localidad')
