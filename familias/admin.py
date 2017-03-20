from django.contrib import admin
from .models import Familia, Alumno, Tutor, Comentario, Integrante

admin.site.register(Familia)
admin.site.register(Integrante)
admin.site.register(Alumno)
admin.site.register(Tutor)
admin.site.register(Comentario)
