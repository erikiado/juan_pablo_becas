from django.contrib import admin
from .models import Periodo, Transaccion, Ingreso

admin.site.register(Periodo)
admin.site.register(Transaccion)
admin.site.register(Ingreso)
