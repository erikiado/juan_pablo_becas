from django.contrib import admin
from .models import Oficio, Periodo, Transaccion, Ingreso

admin.site.register(Oficio)
admin.site.register(Periodo)
admin.site.register(Transaccion)
admin.site.register(Ingreso)
