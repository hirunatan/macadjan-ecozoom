# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from macadjan.models import Entity


class MapSource(models.Model):
    '''
    A people group in charge of collecting and processing entities.
    '''
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'))
    slug = models.SlugField(max_length = 100, null = False, blank = True, unique = True,
            verbose_name = _(u'Slug'))
    description = models.TextField(null = False, blank = True,
            verbose_name = _(u'Descripción'))
    web = models.URLField(null = False, blank = True, default = '',
            verbose_name = _(u'Web'),
            help_text = _(u'Página web informativa. Ojo: hay que poner la dirección completa, incluyendo http://. La dirección será validada automáticamente para comprobar que existe.'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _(u'fuente de mapeo')
        verbose_name_plural = _(u'fuentes de mapeo')


class EcozoomEntity(Entity):

    # Detailed descriptive info
    creation_year = models.IntegerField(null = True, blank = True,
            verbose_name = _(u'Año creación'),
            help_text = _(u'Año en que el colectivo u organización comenzó su actividad (introducir un nº con las cuatro cifras).'))
    legal_form = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Forma jurídica'),
            help_text = _(u'Con qué forma jurídica concreta está registrada la entidad, si lo está.'))
    description = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Descripción'),
            help_text = _(u'Aquí se puede poner una descripción general, o cualquier cosa que no entre en las casillas siguientes. Si hay poca información, puede ser suficiente con rellenar esta casilla. Alternativamente, puede no ser necesaria si se han rellenado las otras con mucha información.'))
    goals = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Objetivo como entidad'),
            help_text = _(u'Objetivos principales de la entidad, cuál es su razón de ser; qué ofrece a sus socios, usuarios, clientes o público en general.'))
    finances = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Finanzas'),
            help_text = _(u'Indicar cómo gestiona el dinero (con/sin ánimo de lucro, precios de los productos si vende algo, fuentes de ingresos, modo de financiación...).'))
    social_values = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Valores sociales y medioambientales'),
            help_text = _(u'Justificación de por qué merece estar en este directorio, valores que aporta en función de nuestros criterios de selección, en tanto que relaciones humanas y cuidado del medio ambiente.'))
    how_to_access = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Forma de acceso'),
            help_text = _(u'Cómo acceder a los servicios o funciones de la entidad, horarios y lugar de contacto, condiciones de participación, venta o ditribución.'))
    networks_member = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Redes de las que forma parte'),
            help_text = _(u'Indicar si esta entidad está integrada en algún tipo de redes, grupo o plataforma, junto con otras entidades.'))
    networks_works_with = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Otras entidades con las que colabora'),
            help_text = _(u'Indicar si esta entidad trabaja en colaboración con otras entidades o redes, aún sin formar parte de ellas.'))
    ongoing_projects = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Proyectos en marcha'),
            help_text = _(u'Indicar, si se desea, los proyectos importantes que la entidad lleva a cabo o en los que está involucrada.'))
    needs = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Necesidades'),
            help_text = _(u'Indicar si la entidad tiene actualmente alguna necesidad importante que pudiera ser cubierta por otras entidades o personas externas.'))
    offerings = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Qué ofrece'),
            help_text = _(u'Indicar si esta entidad está en disposición de ofrecer recursos u otros elementos que puedan ser útiles a otras entidades relacionadas o personas externas; posibilidades de colaboración.'))
    additional_info = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Información adicional'),
            help_text = _(u'Cualquier otra información no clasificable en las casillas anteriores.'))

    map_source = models.ForeignKey(MapSource, related_name = 'entities', null = True, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Fuente'),
            help_text = _('Colectivo encargado de crear y mantener los datos de esta entidad.'))

    class Meta(Entity.Meta):
        ordering = ['name']
        verbose_name = _(u'entidad')
        verbose_name_plural = _(u'entidades')

