# -*- coding: utf-8 -*-

import os.path
import csv

from datetime import datetime

from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from macadjan import models
from .converter_base import EntityConverter

class EntityConverterDefault(EntityConverter):
    '''
    Subclass of EntityConverter that use EntityArchiveCSV to read a spreadsheet
    with the default Macadjan format and convert to entities.
    '''
    def initialize(self, archive):
        archive.configure(_(u'Nombre'), _(u'Categorías'))
        archive_columns = set(archive.column_names())
        if len(archive_columns) < 2:
            raise ValueError(_(u'El archivo no es un csv con el formato esperado'))
        needed_columns = set((
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
            _(u'Persona de contacto'),
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
        ))
        if not needed_columns.issubset(archive_columns):
            raise ValueError(_(u'El archivo no es un csv válido de Macadjan versión 03/04/2012, no se encuentran las siguientes columnas: %(missing_columns)s') %
                    {'missing_columns': ','.join(list(needed_columns.difference(archive_columns)))})

    def get_slug_from_item(self, item):
        '''
        Given an archive item, return the slug, to check if it exists or not
        in Macadjan database.
        '''
        return slugify(item[_(u'Nombre')])

    def load_entity_from_item(self, entity, item):
        '''
        Given an archive item, copy all the available fields to the entity.

        Then, return the modified entity and a list with the many-to-many relations
        that must be filled in (currently only subcategory).

        So the return value is (entity, {'subcategories': [subcategory1, subcategory2,...]})
        '''
        entity.map_source = self.map_source
        entity.name = item[_(u'Nombre')]
        entity.slug = slugify(item[_(u'Nombre')])
        entity.alias = u''
        entity.summary = item[_(u'Resumen')]
        entity.is_container = False
        entity.contained_in = None
        entity.address_1 = item[_(u'Dirección (calle y nº)')]
        entity.address_2 = item[_(u'Dirección (resto)')]
        entity.zipcode = item[_(u'C.P.')]
        entity.city = item[_(u'Población')]
        entity.province = item[_(u'Provincia')]
        entity.country = 'España'
        entity.zone = item[_(u'Zona')]
        lat_str = item.get(_(u'Latitud'), '')
        if lat_str:
            try:
                entity.latitude = float(lat_str.replace(',', '.'))
            except ValueError:
                raise ValueError(_(u'Valor de latitud incorrecto %(lat)s') % {'lat': lat_str})
        else:
            entity.latitude = None
        long_str = item.get(_(u'Longitud'), '')
        if long_str:
            try:
                entity.longitude = float(long_str.replace(',', '.'))
            except ValueError:
                raise ValueError(_(u'Valor de longitud incorrecto %(long)s') % {'long': long_str})
        else:
            entity.longitude = None
        entity.contact_phone_1 = item[_(u'Teléfono 1')]
        entity.contact_phone_2 = item[_(u'Teléfono 2')]
        entity.fax = item[_(u'Fax')]
        entity.email = item[_(u'Correo electrónico 1')]
        entity.email_2 = item[_(u'Correo electrónico 2')]
        entity.web = item[_(u'Web 1')]
        entity.web_2 = item[_(u'Web 2')]
        entity.contact_person = item[_(u'Persona de contacto')]
        creation_year_str = item[_(u'Año de creación')]
        if creation_year_str:
            try:
                entity.creation_year = int(creation_year_str)
                if entity.creation_year < 1000:
                    raise ValueError()
            except ValueError:
                raise ValueError(_(u'El año de creación debe ser un nº de cuatro dígitos'))
        else:
            entity.creation_year = None
        entity.legal_form = item[_(u'Forma jurídica')]
        entity.description = item[_(u'Descripción general')]
        entity.goals = item[_(u'Objetivo como entidad')]
        entity.finances = item[_(u'Finanzas')]
        entity.social_values = item[_(u'Valores sociales y medioambientales')]
        entity.how_to_access = item[_(u'Forma de acceso')]
        entity.networks_member = item[_(u'Redes de las que forma parte')]
        entity.networks_works_with = item[_(u'Otras entidades con las que colabora')]
        entity.ongoing_projects = item[_(u'Proyectos en marcha')]
        entity.needs = item[_(u'Necesidades')]
        entity.offerings = item[_(u'Ofrecimientos')]
        entity.additional_info = item[_(u'Información adicional')]
        modification_date_str = item[_(u'Fecha última actualización')]
        if modification_date_str:
            try:
                entity.modification_date = datetime.strptime(modification_date_str, '%d/%m/%Y')
            except ValueError:
                raise ValueError(_(u'Fecha de última actualización incorrecta, el formato debe ser DD/MM/YYYY'))
        else:
            entity.modification_date = None
        if not entity.creation_date:
            entity.creation_date = entity.modification_date
        type_name = item[_(u'Tipo de entidad')]
        try:
            entity.entity_type = models.EntityType.objects.get(name = type_name)
        except models.EntityType.DoesNotExist:
            raise ValueError(_(u'No se encuentra el tipo de entidad %(type)s') % {'type': type_name})

        # leave is_active as default

        subcategories = []
        for cat_string in item[_(u'Categorías')]:
            cat_pieces = cat_string.replace(u'\u2013', '-').split(' - ')  # Sometimes Excel replaces ascii '-' with unicode '-'
            if len(cat_pieces) != 2:
                raise ValueEror(_(u'Las categorías deben ser dos frases separadas por un guión "-"'))
            cat_name, subcat_name = cat_pieces
            try:
                subcat = models.SubCategory.objects.get(name = subcat_name, category__name = cat_name)
            except models.SubCategory.DoesNotExist:
                raise ValueError(_(u'No se encuentra la categoría %(cat)s - %(subcat)s') %
                                  {'cat': cat_name, 'subcat': subcat_name})
            subcategories.append(subcat)
            if not entity.main_subcategory:
                entity.main_subcategory = subcat

        return (entity, {'subcategories': subcategories})

