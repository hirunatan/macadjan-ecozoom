# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from macadjan.views import EntitiesText, EntitiesList, Entity
from macadjan.views import EntitiesKml, EntitiesGeoRSS, Entities
from macadjan.models import MapSource

import csv

from .models import EcozoomEntity

class EcozoomEntitiesText(EntitiesText):
    model = EcozoomEntity

class EcozoomEntitiesList(EntitiesList):
    model = EcozoomEntity

class EcozoomEntitiesKml(EntitiesKml):
    model = EcozoomEntity

class EcozoomEntitiesGeoRSS(EntitiesGeoRSS):
    model = EcozoomEntity

class UTF8Writer:
    def __init__(self, stream, *args, **kwargs):
        self.writer = csv.writer(stream, *args, **kwargs)

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode('utf-8') for s in row])

class EcozoomEntitiesCSV(Entities):
    '''Get entities in csv format with all columns.'''

    model = EcozoomEntity

    def get(self, request, *args, **kwargs):
        entities_list = self.find_entities(request, *args, **kwargs)

        import cStringIO
        string_buffer = cStringIO.StringIO()

        writer = UTF8Writer(string_buffer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow([
            u'Nombre',
            u'Resumen',
            u'Tipo de entidad',
            u'Categorías',
            u'Dirección (calle y nº',
            u'Dirección (resto)',
            u'C.P.',
            u'Población',
            u'Provincia',
            u'Zona',
            u'Latitud',
            u'Longitud',
            u'Teléfono 1',
            u'Teléfono 2',
            u'Fax',
            u'Correo electrónico 1',
            u'Correo electrónico 2',
            u'Web 1',
            u'Web 2',
            u'Año de creación',
            u'Forma jurídica',
            u'Descripción general',
            u'Objetivo como entidad',
            u'Finanzas',
            u'Valores sociales y medioambientales',
            u'Forma de acceso',
            u'Redes de las que forma parte',
            u'Otras entidades con las que colabora',
            u'Proyectos en marcha',
            u'Necesidades',
            u'Ofrecimientos',
            u'Información adicional',
            u'Fecha última actualización',
        ])

        for entity in entities_list:
            writer.writerow([
                entity.name,
                entity.summary,
                u'{}'.format(entity.entity_type.name),
                u'{} - {}'.format(entity.main_subcategory.category.name, entity.main_subcategory.name),
                entity.address_1,
                entity.address_2,
                entity.zipcode,
                entity.city,
                entity.province,
                entity.zone,
                entity.latitude,
                entity.longitude,
                entity.contact_phone_1,
                entity.contact_phone_2,
                entity.fax,
                entity.email,
                entity.email_2,
                entity.web,
                entity.web_2,
                entity.creation_year,
                entity.legal_form,
                entity.description,
                entity.goals,
                entity.finances,
                entity.social_values,
                entity.how_to_access,
                entity.networks_member,
                entity.networks_works_with,
                entity.ongoing_projects,
                entity.needs,
                entity.offerings,
                entity.additional_info,
                entity.modification_date,
            ])

        return HttpResponse(string_buffer.getvalue(), content_type='text/csv')

class EcozoomEntity(Entity):
    model = EcozoomEntity

class MapSourceView(TemplateView):
    '''Shows detailed info about one map source'''
    template_name = 'macadjan_ecozoom/map_source.html'

    def get_context_data(self, **kwargs):
        map_source = get_object_or_404(MapSource, slug = kwargs.get('map_source_slug', ''))
        return {'map_source': map_source}

    #def get(self, request, map_source_slug):
    #    map_source = get_object_or_404(MapSource, slug = map_source_slug)
    #    return render_to_response('macadjan_ecozoom/map_source.html',
    #        {'map_source': map_source}, context_instance = RequestContext(request))

