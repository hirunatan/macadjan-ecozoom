# -*- coding: utf-8 -*-

import os.path
import csv
import urllib

from datetime import datetime

from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from macadjan import models
from .converter_base import EntityConverter

class EntityConverter15MpediaAsambleas(EntityConverter):
    '''
    Subclass of EntityConverter that use EntityArchiveCSV to read a csv file exported
    from http://wiki.15m.cc/wiki/Lista_de_asambleas and convert to entities.
    '''
    def initialize(self, archive):
        archive.configure(u'Nombre', u'Nombre')
        archive_columns = set(archive.column_names())
        if len(archive_columns) < 2:
            raise ValueError(_(u'El archivo no es un csv con el formato esperado'))
        needed_columns = set((
            u'Nombre',
            u'Municipio',
            u'Distrito',
            u'Barrio',
            u'Lugar',
            u'Día',
            u'Hora',
            u'Comisiones',
            u'Grupos de trabajo',
            u'Plataformas',
            u'Participa en',
            u'Sitio web',
            u'Lista',
            u'Twitter',
            u'Hashtags',
            u'Facebook',
            u'N-1',
            u'Foro',
            u'Flickr',
            u'Youtube',
            u'Vimeo',
            u'Skype',
            u'Streaming',
            u'Actas',
            u'Calendario',
            u'Coordenadas',
        ))
        if not needed_columns.issubset(archive_columns):
            raise ValueError(_(u'El archivo no es un csv válido de #15Mpedia-acampadas versión 15/04/2013, no se encuentran las siguientes columnas: %(missing_columns)s') %
                    {'missing_columns': ','.join(list(needed_columns.difference(archive_columns)))})

    def get_slug_from_item(self, item):
        '''
        Given an archive item, return the slug, to check if it exists or not
        in Macadjan database.
        '''
        return slugify(item[u'Nombre'])

    def load_entity_from_item(self, entity, item):
        '''
        Given an archive item, copy all the available fields to the entity.

        Then, return the modified entity and a list with the many-to-many relations
        that must be filled in (currently only subcategory).

        So the return value is (entity, {'subcategories': [subcategory1, subcategory2,...]})
        '''
        entity.map_source = self.map_source
        entity.name = item[u'']
        entity.slug = slugify(item[u''])
        entity.alias = u''
        entity.summary = u'Asamblea popular del #15m'
        entity.is_container = False
        entity.contained_in = None
        entity.address_1 = u''
        entity.address_2 = u''
        entity.zipcode = u''
        entity.city = item[u'Municipio']
        entity.province = u''
        entity.country = 'España'
        zonas = []
        if item[u'Distrito']:
            zonas.append(u'Distrito %s' % item[u'Distrito'])
        if item[u'Barrio']:
            zonas.append(u'Barrio %s' % item[u'Barrio'])
        entity.zone = ', '.join(zonas)
        coords = item[u'Coordenadas']
        lat, lon = self.degrees_to_decimal(coords)
        entity.latitude = lat
        entity.longitude = lon
        entity.contact_phone_1 = u''
        entity.contact_phone_2 = u''
        entity.fax = u''
        entity.email = u''
        entity.email_2 = u''
        entity.web = item[u'Sitio web']
        entity.web_2 = u'http://wiki.15m.cc/wiki/%s' % urllib.quote(item[u''].encode('utf-8'))
        entity.creation_year = None
        entity.legal_form = u''
        entity.description = u''
        entity.goals = u''
        entity.finances = u''
        entity.social_values = u''
        accesos = []
        if item[u'Lugar'] or item[u'Día']:
            accesos.append(u'Reuniones')
            if item[u'Lugar']:
                accesos.append(u'- %s' % item[u'Lugar'])
            if item[u'Día']:
                accesos.append(u'- Día(s): %s' % item[u'Día'])
            if item[u'Hora']:
                accesos.append(u'- Hora: %s' % item[u'Hora'])
        if item[u'Lista'] or item[u'Twitter'] or item[u'Hashtags'] or item[u'Facebook'] \
          or item[u'N-1'] or item[u'Foro'] or item[u'Flickr'] or item[u'Youtube'] \
          or item[u'Vimeo'] or item[u'Skype'] or item[u'Streaming'] or item[u'Actas'] \
          or item[u'Calendario']:
              accesos.append(u'En la red')
              if item[u'Lista']:
                  accesos.append(u'- Lista de correo: %s' % self.make_link(item[u'Lista']))
              if item[u'Twitter']:
                  accesos.append(u'- Twitter: %s' % self.make_link(item[u'Twitter']))
              if item[u'Hashtags']:
                  accesos.append(u'- Hashtag(s): %s' % self.make_link(item[u'Hashtags']))
              if item[u'Facebook']:
                  accesos.append(u'- Facebook: %s' % self.make_link(item[u'Facebook']))
              if item[u'N-1']:
                  accesos.append(u'- N-1: %s' % self.make_link(item[u'N-1']))
              if item[u'Foro']:
                  accesos.append(u'- Foro: %s' % self.make_link(item[u'Foro']))
              if item[u'Flickr']:
                  accesos.append(u'- Flickr: %s' % self.make_link(item[u'Flickr']))
              if item[u'Youtube']:
                  accesos.append(u'- Youtube: %s' % self.make_link(item[u'Youtube']))
              if item[u'Vimeo']:
                  accesos.append(u'- Vimeo: %s' % self.make_link(item[u'Vimeo']))
              if item[u'Skype']:
                  accesos.append(u'- Skype: %s' % item[u'Skype'])
              if item[u'Streaming']:
                  accesos.append(u'- Streaming: %s' % self.make_link(item[u'Streaming']))
              if item[u'Actas']:
                  accesos.append(u'- Actas: %s' % self.make_link(item[u'Actas']))
              if item[u'Calendario']:
                  accesos.append(u'- Calendario: %s' % self.make_link(item[u'Calendario']))
        entity.how_to_access = '\n'.join(accesos)
        if item[u'Participa en']:
            entity.networks_member = u'Movimientos en los que participa: %s' % item[u'Participa en']
        else:
            entity.networks_member = u''
        if item[u'Plataformas']:
            entity.networks_works_with = u'Plataformas con las que trabaja: %s' % item[u'Plataformas']
        else:
            entity.networks_works_with = u''
        entity.ongoing_projects = u''
        entity.needs = u''
        entity.offerings = u''
        additional = []
        if item[u'Comisiones']:
            additional.append(u'Comisiones: %s' % item[u'Comisiones'])
        if item[u'Grupos de trabajo']:
            additional.append(u'Grupos de trabajo: %s' % item[u'Grupos de trabajo'])
        entity.additional_info = '\n'.join(additional)
        entity.entity_type = models.EntityType.objects.get(name = u'Asamblea')
        entity.main_subcategory = models.SubCategory.objects.get(slug = 'asamblea-popular')

        return (entity, {'subcategories': [], 'tags': []})

    def degrees_to_decimal(self, coords):
        '''
        Convert a string with format 40° 27' 30" N, 3° 42' 6" O into decimal lat, lon.
        '''
        if not coords.strip():
            return None, None

        pieces = coords.split(' ')
        if len(pieces) != 8:
            raise ValueError('Las coordenadas tienen un formato incorrecto')

        degs = self.check_piece_num(pieces[0], u'°')
        mins = self.check_piece_num(pieces[1], u'\'')
        secs = self.check_piece_num(pieces[2], u'"')
        vert = self.check_piece_str(pieces[3], u'NS')
        lat = degs + (mins * 60 + secs) / 3600
        if vert == u'S':
            lat = -lat

        degs = self.check_piece_num(pieces[4], u'°')
        mins = self.check_piece_num(pieces[5], u'\'')
        secs = self.check_piece_num(pieces[6], u'"')
        hor = self.check_piece_str(pieces[7], u'EO')
        lon = degs + (mins * 60 + secs) / 3600
        if hor == u'O':
            lon = -lon

        return lat, lon

    def check_piece_num(self, piece, char):
        if not piece[:-1].isdigit() or piece[-1] != char:
            raise ValueError('Las coordenadas tienen un formato incorrecto')
        return float(piece[:-1])

    def check_piece_str(self, piece, values):
        if not piece[0] in values:
            raise ValueError('Las coordenadas tienen un formato incorrecto')
        return piece[0]

    def make_link(self, url_string):
        return u'<a href="%s">%s</a>' % (url_string, url_string)

