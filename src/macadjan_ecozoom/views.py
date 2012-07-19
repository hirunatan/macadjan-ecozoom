# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from macadjan.views import EntitiesText, EntitiesList, Entity
from macadjan.views import EntitiesKml, EntitiesGeoRSS

from .models import EcozoomEntity, MapSource

class EcozoomEntitiesText(EntitiesText):
    model = EcozoomEntity

class EcozoomEntitiesList(EntitiesList):
    model = EcozoomEntity

class EcozoomEntitiesKml(EntitiesKml):
    model = EcozoomEntity

class EcozoomEntitiesGeoRSS(EntitiesGeoRSS):
    model = EcozoomEntity

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

