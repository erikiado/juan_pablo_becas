from django.contrib import admin
from .models import Oficio, Familia, Alumno, Tutor, Comentario, Integrante, \
                    Sacramento

admin.site.register(Familia)
admin.site.register(Integrante)
admin.site.register(Alumno)
admin.site.register(Tutor)
admin.site.register(Comentario)
admin.site.register(Oficio)
admin.site.register(Sacramento)
