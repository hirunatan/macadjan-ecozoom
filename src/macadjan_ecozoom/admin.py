# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from macadjan.admin import EntityAdmin

from . import models

class EcozoomEntityAdmin(EntityAdmin):
    list_filter = ('is_active', 'subcategories', 'map_source')

    def get_export_csv_columns(self):
        return [
            _(u'Nombre'),
            _(u'Resumen'),
            _(u'Tipo de entidad'),
            _(u'Categorías'),
            _(u'Agrupada dentro de'),
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
        ]

    def get_export_csv_fields(self, entity):
        return [
            entity.name,
            entity.summary,
            entity.entity_type.name,
            '%s - %s' % (entity.main_subcategory.category.name, entity.main_subcategory.name),
            '',
            entity.address_1,
            entity.address_2,
            entity.zipcode,
            entity.city,
            entity.province,
            entity.zone,
            unicode(entity.latitude) if entity.latitude else '',
            unicode(entity.longitude) if entity.longitude else '',
            entity.contact_phone_1,
            entity.contact_phone_2,
            entity.fax,
            entity.email,
            entity.email_2,
            entity.web,
            entity.web_2,
            unicode(entity.creation_year) if entity.creation_year else '',
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
            entity.modification_date.strftime('%d/%m/%Y'),
        ]

admin.site.register(models.EcozoomEntity, EcozoomEntityAdmin)

