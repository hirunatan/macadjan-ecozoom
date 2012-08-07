# -*- coding: utf-8 -*-

class EntityArchive:
    '''
    An abstract archive that contains entities, stored externally to Macadjan.
    To use it, you must derive a new class implementing all not implemented methods above.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Open the archive and set it ready to read.
        '''
        raise NotImplementedError()

    def next(self):
        '''
        Return the next item of the archive. Raise StopIteration if there
        are no more items.
        '''
        raise NotImplementedError()

    def __iter__(self):
        '''
        Implement the iterator protocol.
        '''
        return self

