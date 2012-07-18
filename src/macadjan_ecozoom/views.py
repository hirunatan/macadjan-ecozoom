# Create your views here.

from macadjan.views import EntitiesText, EntitiesList, Entity
from .models import EcozoomEntity

class EcozoomEntitiesText(EntitiesText):
    model = EcozoomEntity

class EcozoomEntitiesList(EntitiesList):
    model = EcozoomEntity

class EcozoomEntity(Entity):
    model = EcozoomEntity

