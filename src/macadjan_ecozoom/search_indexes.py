# -*- coding: utf-8 -*-

from haystack import indexes
from .models import EcozoomEntity

class EntityIndexes(indexes.SearchIndex, indexes.Indexable):
    '''
    Haystack index information of EcozoomEntity.
    For now, we create a 'text' index with the concatenation of several fields.
    '''
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return EcozoomEntity

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active = True)

