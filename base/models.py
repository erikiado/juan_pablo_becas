from django.db import models


class Tutorial(models.Model):
    """ Model for the tutorials that go on the help section.
    """

    ADMINISTRATION_SECTION = 'administracion'
    CAPTURISTA_SECTION = 'captura'
    DIRECTIVO_SECTION = 'direccion'
    SERVICIOS_ESCOLARES_SECTION = 'servicios escolares'
    GENERAL_SECTION = 'general'

    SECTION_OPTIONS = ((GENERAL_SECTION, 'General'),
                       (ADMINISTRATION_SECTION, 'Administración'),
                       (CAPTURISTA_SECTION, 'Captura'),
                       (DIRECTIVO_SECTION, 'Dirección'),
                       (SERVICIOS_ESCOLARES_SECTION, 'Servicios Esolares'))

    titulo = models.CharField(max_length=80, null=False)
    descripcion = models.TextField()
    video = models.URLField()
    seccion = models.CharField(max_length=80, choices=SECTION_OPTIONS)

    def __str__(self):
        return self.titulo
