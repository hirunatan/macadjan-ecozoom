# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

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
        self.writer.writerow([s.encode('utf-8') for s in row])

class EcozoomEntitiesCSV(Entities):
    '''Get entities in csv format with all columns.'''

    model = EcozoomEntity

    def get(self, request, *args, **kwargs):
        entities_list = self.find_entities(request, *args, **kwargs)

        import cStringIO
        string_buffer = cStringIO.StringIO()

        writer = UTF8Writer(string_buffer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        encoder = codecs.getincrementalencoder('utf-8')

        writer.writerow([
            _(u'Nombre'),
            _(u'Resumen'),
            _(u'Tipo de entidad'),
            _(u'Categorías'),
            _(u'Dirección (calle y nº)'),
            _(u'Dirección (resto)'),
            _(u'C.P.'),
            _(u'Población'),
            _(u'Provincia'),
            _(u'Zona'),
            _(u'Latitud'),
            _(u'Longitud'),
            _(u'Teléfono 1'),
            _(u'Teléfono 2'),
            _(u'Fax'),
            _(u'Correo electrónico 1'),
            _(u'Correo electrónico 2'),
            _(u'Web 1'),
            _(u'Web 2'),
            _(u'Año de creación'),
            _(u'Forma jurídica'),
            _(u'Descripción general'),
            _(u'Objetivo como entidad'),
            _(u'Finanzas'),
            _(u'Valores sociales y medioambientales'),
            _(u'Forma de acceso'),
            _(u'Redes de las que forma parte'),
            _(u'Otras entidades con las que colabora'),
            _(u'Proyectos en marcha'),
            _(u'Necesidades'),
            _(u'Ofrecimientos'),
            _(u'Información adicional'),
            _(u'Fecha última actualización'),
        ])

        for entity in entities_list:
            writer.writerow([
                entity.name,
                entity.summary,
                '{}'.format(entity.entity_type.name),
                '{} - {}'.format(entity.main_subcategory.category.name, entity.main_subcategory.name),
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

