# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from macadjan_ecozoom.models import EcozoomEntity
from macadjan_importer.archive_csv import EntityArchiveCSV

import requests
import urllib2

VERSION = 1

class Command(BaseCommand):
    args = ''
    help = 'Upload entities to 15MPedia'

    def handle(self, *args, **options):

        if len(args) != 1:
           return 'You need to give the path to the csv file to send.\n'

        self.csv_file_path = args[0]
        self.csv_file = EntityArchiveCSV(self.csv_file_path)
        self.csv_file.configure(u'Nombre', u'Categorías')

        # Desactivado por seguridad
        # for entity in list(self.csv_file):
        #     print '=================================================='
        #     print entity['Nombre']
        #     print '=================================================='
        #     self.update_entity(entity)


    def update_entity(self, entity):
        page_id = entity[u'Nombre']
        page_title = entity[u'Nombre']

        if entity[u'Categorías'][0] == 'Banco de tiempo - Comunitario':
            tipo_de_gestion = 'Comunitaria'
        elif entity[u'Categorías'][0] == 'Banco de tiempo - Municipal':
            tipo_de_gestion = 'Pública'
        else:
            tipo_de_gestion = ''

        attributes = {
            u'nombre': entity[u'Nombre'], # REVISAR EN EL CSV
            u'descripción': entity[u'Resumen'],
            u'tipo de entidad': entity[u'Tipo de entidad'],
            u'tipo de gestión': tipo_de_gestion,
            u'ámbito': u'Ámbito', # AÑADIR AL CSV
            u'estado': u'Activo',
            u'fecha de fundación': entity[u'Año de creación'] + '/01/01' if entity[u'Año de creación'] else '', # REVISAR EN CSV
            u'participa en': entity[u'Redes de las que forma parte'],
            u'colabora con': entity[u'Otras entidades con las que colabora'],
            u'país': u'España',
            u'comunidad autónoma': entity[u'Comunidad autónoma'], # AÑADIR AL CSV
            u'provincia': u'Provincia de ' + entity[u'Provincia'], # REVISAR EN CSV
            u'comarca': entity[u'Comarca'], # AÑADIR AL CSV
            u'municipio': entity[u'Población'],
            u'distrito': entity[u'Distrito'], # AÑADIR AL CSV
            u'barrio': entity[u'Barrio'], # AÑADIR AL CSV
            u'dirección': entity[u'Dirección'], # AÑADIR AL CSV
            u'coordenadas': entity[u'Latitud'] + ',' + entity[u'Longitud'],
            u'lugar': u'', # CARGAR A MANO
            u'día': u'', # CARGAR A MANO
            u'hora': u'', # CARGAR A MANO
            u'sitio web': ', '.join([web for web in [entity[u'Web 1'], entity[u'Web 2']] if web]),
            u'email': ', '.join([email for email in [entity[u'Correo electrónico 1'], entity[u'Correo electrónico 2']] if email]),
            u'teléfono': ', '.join([phone for phone in [entity[u'Teléfono 1'], entity[u'Teléfono 2']] if phone]),
            u'fax': entity[u'Fax'],
        }
        history = entity[u'Descripción general'] if entity[u'Descripción general'] else u'{{expandir}}'
        organization = u'{{expandir}}'

        self.update_form(page_id = page_id, attributes = attributes)
        self.update_content(page_title = page_title, history = history, organization = organization)


    def update_form(self, page_id, attributes):
        url = 'http://15mpedia.org/w/api.php?action=sfautoedit&form=Banco_de_tiempo&target={page_id}&format=json&query={query}'.format(
            page_id = urllib2.quote(page_id.encode('utf-8')),
            query = '%26'.join([
                'Infobox_Banco_de_tiempo[{}]={}'.format(
                    urllib2.quote(key.encode('utf-8')),
                    urllib2.quote(value.format(v = VERSION).encode('utf-8'))
                ) for key, value in attributes.items()
            ]),
        )

        print '************* update form **************'
        print(url)
        r = requests.get(url)
        print(r.status_code)
        print(r.text)

    def update_content(self, page_title, history, organization):
        content = self.get_content(page_title)
        token = self.get_token(page_title)
        self.update_wikitext(page_title, content, token, history, organization)

    def get_content(self, page_title):
        url = 'http://15mpedia.org/w/api.php?action=query&titles={page_title}&prop=revisions&rvprop=content&format=json'.format(
            page_title=urllib2.quote(page_title.encode('utf-8')),
        )

        print '************* get content **************'
        print(url)
        r = requests.get(url)
        print(r.status_code)
        print(r.json())
        for page_info in r.json()['query']['pages'].values():
            content = page_info['revisions'][0]['*']

        return content

    def get_token(self, page_title):
        url = 'http://15mpedia.org/w/api.php?action=query&titles={page_title}&prop=info&inprop=&intoken=edit&format=json'.format(
            page_title=urllib2.quote(page_title.encode('utf-8')),
        )

        print '************* get token **************'
        print(url)
        r = requests.get(url)
        print(r.status_code)
        print(r.json())

        for page_info in r.json()['query']['pages'].values():
            token = page_info['edittoken']

        return token

    def update_wikitext(self, page_title, content, token, history, organization):
        content = self.replace_between(content, u'== Historia ==', u'== Organización ==', history)
        content = self.replace_between(content, u'== Organización ==', u'=== Tipo de gestión ===', organization)

        # token needs to be the last parameter
        url = 'http://15mpedia.org/w/api.php?action=edit&title={page_title}&format=json&bot&contentformat={content_format}&text={text}&token={token}'.format(
            page_title = urllib2.quote(page_title.encode('utf-8')),
            content_format = urllib2.quote('text/x-wiki'.encode('utf-8')),
            token = urllib2.quote(token.encode('utf-8')),
            text = urllib2.quote(content.encode('utf-8')),
        )

        print '************* update wikitext **************'
        print(url)
        r = requests.post(url)
        print(r.status_code)
        print(r.text)

    def replace_between(self, content, begin, end, text):
        begin_pos = content.index(begin)
        end_pos = content.index(end)
        if begin_pos >= 0 and end_pos >= 0:
            content_before = content[:begin_pos + len(begin)]
            content_after = content[end_pos:]
            return content_before + u'\n\n' + text + u'\n\n' + content_after
        else:
            return content

"""
{{Infobox Banco de tiempo
|nombre=este es el nombre 1
|descripción=esta es la descripción 1
|tipo de entidad=Centro social
|tipo de gestión=Pública
|ámbito=Municipio
|estado=Activo
|fecha de fundación=2015/01/01
|participa en=este es el participa en 1
|colabora con=este es el colabora con 1
|país=España
|comunidad autónoma=Principado de Asturias
|provincia=Provincia de Almería
|comarca=esta es la comarca 1
|municipio=este es el municipio 1
|distrito=este es el distrito 1
|barrio=este es el barrio 1
|dirección=esta es la dirección 1
|coordenadas=estas son las coordenadas 1
|lugar=este es el lugar 1
|día=este es el día 1
|hora=esta es la hora 1
|sitio web=este es el sitio web 1
|email=este es el email 1
|teléfono=este es el teléfono 1
|fax=este es el fax 1
}}
El '''{{PAGENAME}}''' es un [[banco de tiempo]].

== Historia ==
{{expandir}}

== Organización ==
{{expandir}}

=== Tipo de gestión ===
{{expandir}}

=== Condiciones de participación ===
{{expandir}}

== Actividad ==
{{expandir}}

== Documentos ==
{{expandir}}

== Véase también ==
* [[Lista de bancos de tiempo]]

== Referencias ==
{{reflist}}

== Noticias relacionadas ==
{{main|Lista de noticias}}
{{expandir lista}}

== Enlaces externos ==
{{enlaces externos}}

{{bancos de tiempo}}

[[Categoría:Bancos de tiempo]]
"""

