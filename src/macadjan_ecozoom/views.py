# Create your views here.

from macadjan.views import EntitiesText, EntitiesList, Entity
from macadjan.views import EntitiesKml, EntitiesGeoRSS
from .models import EcozoomEntity

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

