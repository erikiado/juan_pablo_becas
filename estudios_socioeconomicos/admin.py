from django.contrib import admin
from .models import Estudio, Seccion, Subseccion, Pregunta, OpcionRespuesta, Respuesta
from .models import Foto

admin.site.register(Estudio)
admin.site.register(Seccion)
admin.site.register(Subseccion)
admin.site.register(Pregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(Respuesta)
admin.site.register(Foto)
