# -*- coding: utf-8 -*-

import os.path
import csv
import urllib

from datetime import datetime

from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from macadjan import models
from .converter_base import EntityConverter

# Problemas:
#  Falta Categoría
#  Todas las filas deben tener nombre comercial (si es igual, repetir)
#  Sí No (también en contenidos)
#  Núm trabajadoras/trabajadores
#  Espaciado inconsistente
#  C.P (falta un punto)
#  El % de recursos en entidades éticas debe ser un número siempre
C_MARCA_TEMPORAL = u'Marca temporal'
C_NOMBRE_ENTIDAD = u'Nombre de la entidad'
C_NOMBRE_COMERCIAL = u'Nombre comercial'
C_CATEGORIA = u'Categoría'
C_FORMA_JURIDICA = u'Forma jurídica'
C_AMBITO_ACTIVIDAD = u'Ámbito de actividad'
C_TIPO_DE_PRODUCTOS = u'Descripción del tipo de productos/servicios que ofrece'
C_FORTALEZAS = u'Fortalezas'
C_DIRECCION_CALLE_NUM = u'Dirección( Calle, Número)'
C_DIRECCION_RESTO = u'Dirección Resto'
C_CP = u'C.P'
C_TELEFONO = u'TeléfoNo'
C_CORREO_ELECTRONICO = u'Correo electrónico'
C_REDES_SOCIALES = u'Redes sociales'
C_NUM_PERSONAS_PARTE = u'Número total de personas que forman parte del comercio'
C_NUM_PERSONAS_SOCIAS_TRABAJADORAS = u'Número de personas socias-trabajadoras'
C_NUM_PERSONAS_TRABAJADORAS_ASALARIADAS = u'Número de personas trabajadoras asalariadas'
C_NUM_ORGANIZACIONES_SOCIAS = u'Número de organizaciones socias'
C_PREOCUPA_IMPACTO_AMBIENTAL = u'¿Os preocupa el impacto medioambiental que pueda tener vuestra actividad?'
C_HACE_RECICLAJE_PAPEL = u'¿Se hace reciclaje de papel?'
C_HACE_RECICLAJE_VIDRIO = u'¿Se hace reciclaje de vidrio?'
C_HACE_RECICLAJE_PLASTICO = u'¿Se hace reciclaje de plástico?'
C_HACE_RECICLAJE_TONER = u'¿Se hace reciclaje de tóners?'
C_HACE_RECICLAJE_OTROS = u'¿Se recicla otros elementos? (pilas, aceite, electrodomésticos,...)?'
C_TIENE_EN_CUENTA_CONSUMO_ENERGETICO = u'¿Se tiene en cuenta el consumo energético en el negocio?'
C_ESTRATEGIAS_CONSUMO_ENERGETICO = u'Sí se utilizan estrategias para reducir el consumo energético del establecimiento, especifica cuáles'
C_CONOCE_PROVEEDOR_ENERGIA = u'¿Sabéis cuál es vuestro proveedor de energía eléctrica?'
C_CONOCE_ALTERNATIVAS = u'¿CoNocéis otras alternativas?'
C_CONOCE_ORIGEN_PRODUCTOS = u'¿CoNocéis el origen de los productos que vendéis/transformáis/consumís en vuestra actividad?'
C_CONSIDERA_PROVEEDORES_CERCANOS = u'¿Habéis conSíderado recurrir a otros proveedores más cercaNos?'
C_RAZONES_PROVEEDORES_CERCANOS = u'En caso de responder Sí a la pregunta anterior, razones de la respuesta'
C_TIENE_EN_CUENTA_IMPACTO_TRANSPORTE = u'¿Se tiene en cuenta el impacto medioambiental de los medios de transporte?'
C_IMPACTOS_CONSIDERADOS = u'En caso de responder Sí a la pregunta anterior, indica cuáles'
C_ACCIONES_MEJORA_AMBIENTAL = u'¿Qué acciones de mejora medioambiental ha hecho el establecimiento durante el último año?'
C_COLABORA_CON_OTRA_ORGANIZACION = u'Sí se colabora o participa con alguna asociación, ONG, asamblea de barrio u otra iniciativa social, enumera cuáles y de qué forma se concreta esa labor'
C_TIENE_EN_CUENTA_NECESIDADES_VECINDARIO = u'Sí se tienen en cuenta neceSídades del vecindario, describe de qué manera se tienen en cuenta'
C_TIENE_EN_CUENTA_IMPACTO_ENTORNO = u'Sí se tienen en cuenta impactos en el entorNo, describe cuáles y de qué manera se tienen en cuenta.'
C_ESTRUCTURA_ORGANIZATIVA = u'¿Cuál es la estructura organizativa del establecimiento?'
C_PERSONAS_TRABAJADORAS_RECIBEN_FORMACION = u'¿Las personas trabajadoras reciben algún tipo de formación o curso?'
C_PERSONAS_TRABAJADORAS_ACCIONES_FORMATIVAS = u'Sí las personas trabajadoras reciben formación, indica las actuaciones formativas (en horario laboral o financiadas por el negocio) del último año en las que hayan participado alguna/s de las personas de la entidad'
C_TIPOS_DE_CONTRATO = u'¿Qué tipo/s de contrato/s utilizáis con las personas que trabajan en el establecimiento? Indica tipo de contrato, personas contratadas y horas de contrato.'
C_JORNADAS_LABORALES = u'¿Cómo se organizan las jornadas laborales de las personas trabajadoras? ¿Se permiten flexibilidad de horarios y lugares de trabajo? ¿Se tienen en cuenta las circunstancias personales y familiares a la hora de organizar los horarios?'
C_MECANISMOS_DE_SELECCION = u'¿Qué mecanismo de selección de personal se utilizan?'
C_SE_ADELANTAN_NOMINAS = u'¿Se adelantan nóminas en momentos puntuales?'
C_ESTRATEGIAS_INCENTIVAR_PERSONAS_TRABAJADORAS = u'¿Qué estrategias se utilizan para incentivar a las personas trabajadoras?'
C_NUM_TRABAJADORES_HOMBRES = u'Número total de trabajadores hombres'
C_NUM_TRABAJADORES_HOMBRES_DISCAPACIDAD = u'Número de trabajadoras con discapacidad'
C_NUM_TRABAJADORES_HOMBRES_INMIGRANTES = u'Número de trabajadores inmigrantes'
C_NUM_TRABAJADORES_HOMBRES_MINORIAS = u'Número de trabajadores pertenecientes a miNorías étnicas'
C_NUM_TRABAJADORES_HOMBRES_EXCLUSION = u'Número de trabajadores en riesgo de excluSíón social o en Sítuación de neceSídad'
C_NUM_TRABAJADORES_MUJERES = u'Número total de trabajadoras mujeres'
C_NUM_TRABAJADORES_MUJERES_DISCAPACIDAD = u'Número de trabajadores con discapacidad'
C_NUM_TRABAJADORES_MUJERES_INMIGRANTES = u'Número de trabajadoras pertenecientes a miNorías étnicas'
C_NUM_TRABAJADORES_MUJERES_MINORIAS= u'Número de trabajadoras en riesgo de excluSíón social o en Sítuación de neceSídad'
C_NUM_TRABAJADORES_MUJERES_EXCLUSION = u'Número de trabajadoras inmigrantes'
C_HAY_POLITICA_IGUALDAD = u'¿Hay alguna política de igualdad en el establecimiento?'
C_DESCRIPCION_POLITICA_IGUALDAD = u'Sí la respuesta a la pregunta anterior es "Sí", explica cuáles. Sí la respuesta a la pregunta anterior es "No", explica por qué.'
C_REPRESENTACION_PERSONAS_TRABAJADORAS = u'¿Existe algún mecanismo de representación de las personas trabajadoras?'
C_PARTICIPA_CLIENTELA_O_PROVEEDORES = u'¿Participa o puede participar la clientela del barrio o sus proveedores en alguna deciSíón del establecimiento?'
C_PARTICIPAN_PERSONAS_TRABAJADORAS = u'¿Participa o pueden participar las personas trabajadoras en alguna deciSíón del establecimiento?'
C_SENTIDO_Y_FINALIDAD = u'¿Cuál es el sentido y finalidad del negocio?'
C_QUE_TRATA_DE_APORTAR = u'¿Qué trata de aportar este establecimiento al barrio, a los veciNos/as,...?'
C_LE_GUSTARIA_MARCARSE_OBJETIVOS = u'¿Al establecimiento le gustaría y estaría dispuesto a marcarse objetivos para mejorar la vida de las personas del barrio?'
C_CUALES_OBJETIVOS = u'En caso de responder "Sí" a la pregunta anterior, ¿cuáles serían estos objetivos?'
C_PARTICIPA_CON_OTROS_ESTABLECIMIENTOS = u'¿El establecimiento participa o colabora en proyectos o iniciativas con otros establecimientos Símilares?'
C_CUALES_OTROS_ESTABLECIMIENTOS = u'Sí la respuesta anterior es Sí, ¿cuáles y de qué manera?'
C_CUESTIONARIO_PUBLICO = u'¿El establecimiento está dispuesto a hacer públicos los resultados de este cuestionario?'
C_POR_QUE_NO_PUBLICO = u'Sí responde "No" a la pregunta anterior, explica porqué.'
C_NUM_PROVEEDORES = u'¿De cuántos/as proveedores/as dispone aproximadamente?'
C_NUM_PROVEEDORES_ECONOMIA_ALTERNATIVA = u'¿Cuántos/as de ellos/as pertenecen a la ecoNomía alternativa y solidaria?'
C_NUM_CLIENTES = u'¿De cuántos/as clientes/as disponéis aproximadamente?'
C_NUM_CLIENTES_ECONOMIA_ALTERNATIVA = u'¿Cuántos/as de ellos/as pertenecen a la ecoNomía alternativa y solidaria?'
C_RECURSOS_EN_ENTIDAD_ETICA = u'¿Qué porcentaje de los recursos económicos del establecimiento están depoSítados en una entidad ética?'
C_QUE_ENTIDAD_ETICA = u'En caso de depoSítar recursos económicos en entidades éticas, indica cuál/es'
C_USA_SOFTWARE_LIBRE = u'¿Utiliza la entidad software libre en sus equipos informáticos?'
C_USA_LICENCIAS_LIBRES = u'¿Utiliza el establecimiento licencias libres (copyleft)?'


class EntityConverterMSMalasana(EntityConverter):
    '''
    Subclass of EntityConverter that use EntityArchiveCSV to read a csv file exported
    from MS Malasaña spreadsheet and convert to entities.
    '''
    def initialize(self, archive):
        archive.configure(C_NOMBRE_COMERCIAL, C_CATEGORIA)
        archive_columns = set(archive.column_names())
        if len(archive_columns) < 2:
            raise ValueError(_(u'El archivo no es un csv con el formato esperado'))
        needed_columns = set((
            C_MARCA_TEMPORAL,
            C_NOMBRE_ENTIDAD,
            C_NOMBRE_COMERCIAL,
            C_CATEGORIA,
            C_FORMA_JURIDICA,
            C_AMBITO_ACTIVIDAD,
            C_TIPO_DE_PRODUCTOS,
            C_FORTALEZAS,
            C_DIRECCION_CALLE_NUM,
            C_DIRECCION_RESTO,
            C_CP,
            C_TELEFONO,
            C_CORREO_ELECTRONICO,
            C_REDES_SOCIALES,
            C_NUM_PERSONAS_PARTE,
            C_NUM_PERSONAS_SOCIAS_TRABAJADORAS,
            C_NUM_PERSONAS_TRABAJADORAS_ASALARIADAS,
            C_NUM_ORGANIZACIONES_SOCIAS,
            C_PREOCUPA_IMPACTO_AMBIENTAL,
            C_HACE_RECICLAJE_PAPEL,
            C_HACE_RECICLAJE_VIDRIO,
            C_HACE_RECICLAJE_PLASTICO,
            C_HACE_RECICLAJE_TONER,
            C_HACE_RECICLAJE_OTROS,
            C_TIENE_EN_CUENTA_CONSUMO_ENERGETICO,
            C_ESTRATEGIAS_CONSUMO_ENERGETICO,
            C_CONOCE_PROVEEDOR_ENERGIA,
            C_CONOCE_ALTERNATIVAS,
            C_CONOCE_ORIGEN_PRODUCTOS,
            C_CONSIDERA_PROVEEDORES_CERCANOS,
            C_RAZONES_PROVEEDORES_CERCANOS,
            C_TIENE_EN_CUENTA_IMPACTO_TRANSPORTE,
            C_IMPACTOS_CONSIDERADOS,
            C_ACCIONES_MEJORA_AMBIENTAL,
            C_COLABORA_CON_OTRA_ORGANIZACION,
            C_TIENE_EN_CUENTA_NECESIDADES_VECINDARIO,
            C_TIENE_EN_CUENTA_IMPACTO_ENTORNO,
            C_ESTRUCTURA_ORGANIZATIVA,
            C_PERSONAS_TRABAJADORAS_RECIBEN_FORMACION,
            C_PERSONAS_TRABAJADORAS_ACCIONES_FORMATIVAS,
            C_TIPOS_DE_CONTRATO,
            C_JORNADAS_LABORALES,
            C_MECANISMOS_DE_SELECCION,
            C_SE_ADELANTAN_NOMINAS,
            C_ESTRATEGIAS_INCENTIVAR_PERSONAS_TRABAJADORAS,
            C_NUM_TRABAJADORES_HOMBRES,
            C_NUM_TRABAJADORES_HOMBRES_DISCAPACIDAD,
            C_NUM_TRABAJADORES_HOMBRES_INMIGRANTES,
            C_NUM_TRABAJADORES_HOMBRES_MINORIAS,
            C_NUM_TRABAJADORES_HOMBRES_EXCLUSION,
            C_NUM_TRABAJADORES_MUJERES,
            C_NUM_TRABAJADORES_MUJERES_DISCAPACIDAD,
            C_NUM_TRABAJADORES_MUJERES_INMIGRANTES,
            C_NUM_TRABAJADORES_MUJERES_MINORIAS,
            C_NUM_TRABAJADORES_MUJERES_EXCLUSION,
            C_HAY_POLITICA_IGUALDAD,
            C_DESCRIPCION_POLITICA_IGUALDAD,
            C_REPRESENTACION_PERSONAS_TRABAJADORAS,
            C_PARTICIPA_CLIENTELA_O_PROVEEDORES,
            C_PARTICIPAN_PERSONAS_TRABAJADORAS,
            C_SENTIDO_Y_FINALIDAD,
            C_QUE_TRATA_DE_APORTAR,
            C_LE_GUSTARIA_MARCARSE_OBJETIVOS,
            C_CUALES_OBJETIVOS,
            C_PARTICIPA_CON_OTROS_ESTABLECIMIENTOS,
            C_CUALES_OTROS_ESTABLECIMIENTOS,
            C_CUESTIONARIO_PUBLICO,
            C_POR_QUE_NO_PUBLICO,
            C_NUM_PROVEEDORES,
            C_NUM_PROVEEDORES_ECONOMIA_ALTERNATIVA,
            C_NUM_CLIENTES,
            C_NUM_CLIENTES_ECONOMIA_ALTERNATIVA,
            C_RECURSOS_EN_ENTIDAD_ETICA,
            C_QUE_ENTIDAD_ETICA,
            C_USA_SOFTWARE_LIBRE,
            C_USA_LICENCIAS_LIBRES,
        ))
        if not needed_columns.issubset(archive_columns):
            raise ValueError(_(u'El archivo no es un csv válido de MS Malasaña versión 5/04/2014, no se encuentran las siguientes columnas: %(missing_columns)s') %
                    {'missing_columns': ','.join(list(needed_columns.difference(archive_columns)))})

    def get_slug_from_item(self, item):
        '''
        Given an archive item, return the slug, to check if it exists or not
        in Macadjan database.
        '''
        return slugify(item[C_NOMBRE_COMERCIAL])

    def load_entity_from_item(self, entity, item):
        '''
        Given an archive item, copy all the available fields to the entity.

        Then, return the modified entity and a list with the many-to-many relations
        that must be filled in (currently only subcategory).

        So the return value is (entity, {'subcategories': [subcategory1, subcategory2,...]})
        '''
        entity.map_source = self.map_source
        entity.name = item[C_NOMBRE_COMERCIAL]
        entity.slug = self.get_slug_from_item(item)
        entity.alias = item[C_NOMBRE_ENTIDAD]
        entity.summary = item[C_AMBITO_ACTIVIDAD]
        entity.is_container = False
        entity.contained_in = None
        entity.address_1 = item[C_DIRECCION_CALLE_NUM]
        entity.address_2 = item[C_DIRECCION_RESTO]
        entity.zipcode = item[C_CP]
        entity.city = u'Madrid'
        entity.province = u'Madrid'
        entity.country = u'España'
        entity.zone = ''
        entity.contact_phone_1 = item[C_TELEFONO]
        entity.contact_phone_2 = u''
        entity.fax = u''
        entity.email = item[C_CORREO_ELECTRONICO]
        entity.email_2 = u''
        entity.web = u''
        entity.web_2 = u''
        entity.creation_year = None
        entity.legal_form = item[C_FORMA_JURIDICA]
        entity.description = item[C_FORTALEZAS]
        entity.goals = self.compose_list([
            (
                item[C_SENTIDO_Y_FINALIDAD],
                u'Sentido y finalidad del negocio:',
                True, item[C_SENTIDO_Y_FINALIDAD]
            ),(
                item[C_QUE_TRATA_DE_APORTAR],
                u'Qué trata de aportar al barrio o a los vecinos/as:',
                True, item[C_QUE_TRATA_DE_APORTAR]
            ),(
                item[C_LE_GUSTARIA_MARCARSE_OBJETIVOS],
                u'Le gustaría marcarse objetivos para mejorar la vida de las personas del barrio.',
                True, item[C_CUALES_OBJETIVOS]
            ),
        ])
        entity.finances = self.compose_list([
            (
                self.to_float(item[C_RECURSOS_EN_ENTIDAD_ETICA]),
                u'Porcentaje de recursos económicos depositados en una entidad ética:',
                False, (u'%d%%' % (self.to_float(item[C_RECURSOS_EN_ENTIDAD_ETICA]) * 100)) if item[C_RECURSOS_EN_ENTIDAD_ETICA] else u''
            ),
            (
                item[C_QUE_ENTIDAD_ETICA],
                u'En qué entidad:',
                False, item[C_QUE_ENTIDAD_ETICA]
            ),
        ])
        entity.social_values = self.compose_list([
            (
                item[C_NUM_TRABAJADORES_HOMBRES],
                u'Número de trabajadores hombres:',
                False, item[C_NUM_TRABAJADORES_HOMBRES]
            ),(
                item[C_NUM_TRABAJADORES_HOMBRES_DISCAPACIDAD],
                u'Número de trabajadores hombres con discapacidad:',
                False, item[C_NUM_TRABAJADORES_HOMBRES_DISCAPACIDAD]
            ),(
                item[C_NUM_TRABAJADORES_HOMBRES_INMIGRANTES],
                u'Número de trabajadores hombres inmigrantes:',
                False, item[C_NUM_TRABAJADORES_HOMBRES_INMIGRANTES]
            ),(
                item[C_NUM_TRABAJADORES_HOMBRES_MINORIAS],
                u'Número de trabajadores hombres pertenecientes a minorías étnicas:',
                False, item[C_NUM_TRABAJADORES_HOMBRES_MINORIAS]
            ),(
                item[C_NUM_TRABAJADORES_HOMBRES_EXCLUSION],
                u'Número de trabajadores hombres en riesgo de exclusión social:',
                False, item[C_NUM_TRABAJADORES_HOMBRES_EXCLUSION]
            ),(
                item[C_NUM_TRABAJADORES_MUJERES],
                u'Número de trabajadores mujeres:',
                False, item[C_NUM_TRABAJADORES_MUJERES]
            ),(
                item[C_NUM_TRABAJADORES_MUJERES_DISCAPACIDAD],
                u'Número de trabajadores mujeres con discapacidad:',
                False, item[C_NUM_TRABAJADORES_MUJERES_DISCAPACIDAD]
            ),(
                item[C_NUM_TRABAJADORES_MUJERES_INMIGRANTES],
                u'Número de trabajadores mujeres inmigrantes:',
                False, item[C_NUM_TRABAJADORES_MUJERES_INMIGRANTES]
            ),(
                item[C_NUM_TRABAJADORES_MUJERES_MINORIAS],
                u'Número de trabajadores mujeres pertenecientes a minorías étnicas:',
                False, item[C_NUM_TRABAJADORES_MUJERES_MINORIAS]
            ),(
                item[C_NUM_TRABAJADORES_MUJERES_EXCLUSION],
                u'Número de trabajadores mujeres en riesgo de exclusión social:',
                False, item[C_NUM_TRABAJADORES_MUJERES_EXCLUSION]
            ),(
                item[C_HAY_POLITICA_IGUALDAD],
                u'Hay alguna política de igualdad en el establecimiento:',
                False, item[C_HAY_POLITICA_IGUALDAD]
            ),(
                item[C_DESCRIPCION_POLITICA_IGUALDAD],
                u'Cuál / por qué no:',
                False, item[C_DESCRIPCION_POLITICA_IGUALDAD]
            ),(
                item[C_REPRESENTACION_PERSONAS_TRABAJADORAS],
                u'Existe un mecanismo de representación de las personas trabajadoras.',
                False, u''
            ),(
                item[C_PARTICIPAN_PERSONAS_TRABAJADORAS],
                u'Las personas trabajadoras tienen participación en decisiones del establecimiento.',
                False, u''
            ),(
                item[C_PARTICIPA_CLIENTELA_O_PROVEEDORES],
                u'La clientela del barrio o los proveedores tienen participación en decisiones del establecimiento.',
                False, u''
            ),(
                item[C_PREOCUPA_IMPACTO_AMBIENTAL],
                u'El establecimiento se preocupa por el impacto ambiental de su actividad.',
                False, u''
            ),(
                item[C_HACE_RECICLAJE_PAPEL],
                u'El establecimiento hace reciclaje de papel.',
                False, u''
            ),(
                item[C_HACE_RECICLAJE_VIDRIO],
                u'El establecimiento hace reciclaje de vidrio.',
                False, u''
            ),(
                item[C_HACE_RECICLAJE_PLASTICO],
                u'El establecimiento hace reciclaje de plástico.',
                False, u''
            ),(
                item[C_HACE_RECICLAJE_TONER],
                u'El establecimiento hace reciclaje de toners.',
                False, u''
            ),(
                item[C_HACE_RECICLAJE_OTROS],
                u'El establecimiento hace reciclaje de otros elementos (pilas, aceite, electrodomésticos...).',
                False, u''
            ),(
                item[C_TIENE_EN_CUENTA_CONSUMO_ENERGETICO],
                u'El establecimiento tiene en cuenta el consumo energético del establecimiento.',
                False, u''
            ),(
                item[C_ESTRATEGIAS_CONSUMO_ENERGETICO],
                u'Estrategias para reducir el consumo energético del establecimiento:',
                True, item[C_ESTRATEGIAS_CONSUMO_ENERGETICO]
            ),(
                item[C_CONOCE_PROVEEDOR_ENERGIA],
                u'El establecimiento conoce su proveedor de energía eléctrica.',
                False, u''
            ),(
                item[C_CONOCE_ALTERNATIVAS],
                u'El establecimiento conoce los proveedores de energía eléctrica alternativos.',
                False, u''
            ),(
                item[C_CONOCE_ORIGEN_PRODUCTOS],
                u'El establecimiento conoce el origen de los productos que vende/transforma/consume en su actividad.',
                False, u''
            ),(
                item[C_CONSIDERA_PROVEEDORES_CERCANOS],
                u'El establecimiento considera recurrir a proveedores cercanos.',
                True, item[C_RAZONES_PROVEEDORES_CERCANOS]
            ),(
                item[C_TIENE_EN_CUENTA_IMPACTO_TRANSPORTE],
                u'El establecimiento tiene en cuenta el impacto medioambiental de los medios de transporte.',
                True, item[C_IMPACTOS_CONSIDERADOS]
            ),(
                item[C_ACCIONES_MEJORA_AMBIENTAL],
                u'Acciones de mejora medioambiental durante el ultimo año:',
                True, item[C_ACCIONES_MEJORA_AMBIENTAL]
            ),(
                item[C_TIENE_EN_CUENTA_NECESIDADES_VECINDARIO],
                u'El establecimiento tiene en cuenta las necesidades del vecindario:',
                True, item[C_TIENE_EN_CUENTA_NECESIDADES_VECINDARIO]
            ),(
                item[C_TIENE_EN_CUENTA_IMPACTO_ENTORNO],
                u'El establecimiento tiene en cuenta el impacto en el entorno:',
                True, item[C_TIENE_EN_CUENTA_IMPACTO_ENTORNO]
            ),(
                item[C_USA_SOFTWARE_LIBRE],
                u'El establecimiento usa software libre en sus equipos informáticos.',
                False, u''
            ),(
                item[C_USA_LICENCIAS_LIBRES],
                u'El establecimiento usa licencias libres (copyleft).',
                False, u''
            )
        ])
        entity.how_to_access = u''
        entity.networks_member = u''
        entity.networks_works_with = self.compose_list([
            (
                item[C_PARTICIPA_CON_OTROS_ESTABLECIMIENTOS],
                u'¿Participa o colabora en proyectos o iniciativas con otros establecimientos similares?',
                True, item[C_CUALES_OTROS_ESTABLECIMIENTOS]
            ),(
                item[C_COLABORA_CON_OTRA_ORGANIZACION],
                u'¿Colabora con alguna asociación, ONG, asamblea de barrio u otra iniciativa social?',
                True, item[C_COLABORA_CON_OTRA_ORGANIZACION]
            ),
        ])
        entity.ongoing_projects = u''
        entity.needs = u''
        entity.offerings = item[C_TIPO_DE_PRODUCTOS]
        entity.additional_info = self.compose_list([
            (
                item[C_REDES_SOCIALES],
                u'Redes sociales:',
                False, item[C_REDES_SOCIALES]
            ),(
                item[C_NUM_PERSONAS_PARTE],
                u'Nº total de personas que forman parte del comercio:',
                False, item[C_NUM_PERSONAS_PARTE]
            ),(
                item[C_NUM_PERSONAS_SOCIAS_TRABAJADORAS],
                u'Nº total de personas que son socias-trabajadoras:',
                False, item[C_NUM_PERSONAS_SOCIAS_TRABAJADORAS]
            ),(
                item[C_NUM_PERSONAS_TRABAJADORAS_ASALARIADAS],
                u'Nº total de personas trabajadoras asalariadas:',
                False, item[C_NUM_PERSONAS_TRABAJADORAS_ASALARIADAS]
            ),(
                item[C_NUM_ORGANIZACIONES_SOCIAS],
                u'Nº total de organizaciones socias:',
                False, item[C_NUM_ORGANIZACIONES_SOCIAS]
            ),(
                item[C_ESTRUCTURA_ORGANIZATIVA],
                u'Estructura organizativa del establecimiento:',
                True, item[C_ESTRUCTURA_ORGANIZATIVA]
            ),(
                item[C_PERSONAS_TRABAJADORAS_RECIBEN_FORMACION],
                u'Las personas trabajadoras han recibido formación a cargo del negocio en el último año.',
                True, item[C_PERSONAS_TRABAJADORAS_ACCIONES_FORMATIVAS]
            ),(
                item[C_TIPOS_DE_CONTRATO],
                u'Tipos de contrato utilzados:',
                True, item[C_TIPOS_DE_CONTRATO]
            ),(
                item[C_JORNADAS_LABORALES],
                u'¿Cómo se organizan las jornadas laborales de las personas trabajadoras?',
                True, item[C_JORNADAS_LABORALES]
            ),(
                item[C_MECANISMOS_DE_SELECCION],
                u'¿Qué mecanismos de selección de personal se utilizan?',
                True, item[C_MECANISMOS_DE_SELECCION]
            ),(
                item[C_SE_ADELANTAN_NOMINAS],
                u'El establecimiento puede adelantar nóminas en momentos puntuales.',
                False, u''
            ),(
                item[C_ESTRATEGIAS_INCENTIVAR_PERSONAS_TRABAJADORAS],
                u'Estrategias para incentivar a las personas trabajadoras',
                True, item[C_ESTRATEGIAS_INCENTIVAR_PERSONAS_TRABAJADORAS]
            ),(
                item[C_NUM_PROVEEDORES],
                u'Nº aproximado de proveedores:',
                False, item[C_NUM_PROVEEDORES]
            ),(
                item[C_NUM_PROVEEDORES_ECONOMIA_ALTERNATIVA],
                u'Cuántos de ellos pertenecen a la economía alternativa y solidaria:',
                False, item[C_NUM_PROVEEDORES_ECONOMIA_ALTERNATIVA]
            ),(
                item[C_NUM_CLIENTES],
                u'Nº aproximado de clientes:',
                False, item[C_NUM_CLIENTES]
            ),(
                item[C_NUM_CLIENTES_ECONOMIA_ALTERNATIVA],
                u'Cuántos de ellos pertenecen a la economía alternativa y solidaria:',
                False, item[C_NUM_CLIENTES_ECONOMIA_ALTERNATIVA]
            ),
        ])
        entity.modification_date = datetime.strptime(item[C_MARCA_TEMPORAL], '%m/%d/%Y %H:%M:%S')
        entity.entity_type = models.EntityType.objects.get(name = u'Empresa/autónomo')
        entity.main_subcategory = models.SubCategory.objects.get(slug = 'comercio-local')

        entity.is_active = True

        return (entity, {'subcategories': [], 'tags': []})

    def compose_list(self, content_list):
        result_list = []
        for condition, title, new_line, content in content_list:
            if condition and condition <> '0' and condition <> 'No':
                result_list.append(
                    u'<li>' +
                    (u'<strong>%s</strong>' % title) +
                    (u'\n%s' % content if content and new_line else u'') +
                    (u' %s' % content if content and not new_line else u'') +
                    u'</li>'
                )
        if result_list:
            return u'<ul>%s</ul>' % (''.join(result_list))
        else:
            return u''

    def to_float(self, float_string):
        return float(float_string.replace(',', '.')) if float_string else 0.0

    def to_int(self, int_string):
        return int(int_string) if int_string else 0

