# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.template import RequestContext, Context, loader

from datetime import datetime

from macadjan.models import EntityType, Category, SubCategory
from macadjan_ecozoom.models import EcozoomEntity, MapSource


# TODO: rethink this so that it does not need a separate model, but use directly EcozoomEntity
#       and if possible, move it to generic macadjan

class EntityProposal(models.Model):
    '''
    A proposal that a external user has made for an entity, via the proposal form. It may be for a new
    entity or to modify data of an existing one.
    '''
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = ((STATUS_PENDING, _(u'Pendiente')),
                      (STATUS_ACCEPTED, _(u'Aceptada')),
                      (STATUS_REJECTED, _(u'Rechazada')))

    # Main info
    existing_entity = models.ForeignKey(EcozoomEntity, related_name = 'change_proposals', null = True, blank = True,
            on_delete = models.SET_NULL,
            verbose_name = _(u'Entidad existente'),
            help_text = _('Indica si esta propuesta es para cambiar los datos de una entidad existente (nulo si es para crear una entidad nueva).'))
    name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Nombre'),
            help_text = _(u'Nombre de la entidad (para salir en el globo).'))

    # Entity type
    entity_type = models.ForeignKey(EntityType, related_name = 'entity_proposals', null = False, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Tipo de entidad'),
            help_text = _(u'De qué tipo organizativo es la entidad, estructuralmente hablando.'))

    # Main subcategory
    main_subcategory = models.ForeignKey(SubCategory, related_name = 'entity_proposals_main', null = False, blank = False,
            on_delete = models.PROTECT,
            limit_choices_to = {'is_active': True},
            verbose_name = _(u'Categoría principal'),
            help_text = _(u'Determinará el tipo de icono en el mapa.'))

    # Proponent info
    proponent_email = models.EmailField(null = False, blank = True, default = '',
            verbose_name = _(u'Email de quien hace la propuesta'),
            help_text = _(u'Si nos indicas tu email, te notificaremos cuando la procesemos y te podremos contactar para resolver dudas.'))
    proponent_comment = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Comentarios de la propuesta'),
            help_text = _(u'Cualquier cosa que nos quieras comentar acerca de la propuesta.'))

    # Accounting info
    status = models.CharField(max_length = 50, null = False, blank = False,
            default = STATUS_CHOICES[0][0],
            choices = STATUS_CHOICES,
            verbose_name = _(u'Estado de la propuesta'))
    status_info = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Respuesta a la propuesta (OJO, SE LE ENVIARÁ POR EMAIL AL PROPONENTE)'),
            help_text = _(u'Comentarios sobre la propuesta o información de por qué se ha aceptado o rechazado.'))
    internal_comment = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Comentarios internos (ESTO NO SALDRÁ DE AQUÍ)'),
            help_text = _(u'Notas internas de los administradores sobre la propuesta.'))
    map_source = models.ForeignKey(MapSource, related_name = 'entity_proposals', null = True, blank = False,
            on_delete = models.PROTECT,
            verbose_name = _(u'Fuente'),
            help_text = _('Colectivo encargado de crear y mantener los datos de esta entidad.'))
    creation_date = models.DateTimeField(null = False, blank = True,
            verbose_name = _(u'Fecha de alta'),
            help_text = _(u'Fecha y hora de envío de esta propuesta.'))
    modification_date = models.DateTimeField(null = False, blank = True,
            verbose_name = _(u'Fecha de última modificación'),
            help_text = _(u'Fecha y hora de última modificación de esta propuesta.'))

    # General description
    alias = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Alias'),
            help_text = _(u'Un posible nombre alternativo para la entidad.'))
    summary = models.CharField(max_length = 300, null = False, blank = True,
            verbose_name = _(u'Resumen'),
            help_text = _(u'Descríbela en una frase.'))

    # Other subcategories
    subcategories = models.ManyToManyField(SubCategory, related_name = 'entity_proposals', blank = True,
            verbose_name = _(u'Categorías'),
            limit_choices_to = {'is_active': True},
            help_text = _(u'Puedes indicar otras categorías para clasificar mejor la entidad, y que aparezca en distintas opciones de búsqueda.'))

    # Geographical info
    address_1 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Dirección (calle y nº)'),
            help_text = _(u'Tipo y nombre de vía y número. Ejemplos: C/ del Pez, 21; Av. de la ilustración, 145'))
    address_2 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Dirección (resto)'),
            help_text = _(u'Portal, piso y otros datos. Ejemplos: Escalera A, 3º izq.; Local 4 entrada posterior'))
    zipcode = models.CharField(max_length = 5, null = False, blank = True, default = '',
            verbose_name = _(u'Cód. postal'),
            help_text = _(u'Cinco dígitos. Ej. 28038'))
    city = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Población'),
            help_text = _(u'Nombre de la población tal como se usa en la dirección postal. Ej. Madrid, Alcorcón.'))
    province = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Provincia'),
            help_text = _(u'Nombre de la provincia, no es necesario si se llama igual que la ciudad.'))
    country = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'País'),
            help_text = _(u'Nombre del país, tal como se usa en la dirección postal, si es necesario.'))
    zone = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Zona'),
            help_text = _(u'Zona de influencia de la entidad. Puede ser barrio, pueblo, ciudad, comarca, pedanía... Ej. Barrio de Lavapiés, Sierra Norte de Madrid.'))
    latitude = models.FloatField(max_length = 100, null = True, blank = True,
            verbose_name = _(u'Latitud'),
            help_text = _(u'Puedes introducir directamente las coordenadas (latitud) si las conoces. Ej. 41.058244'))
    longitude = models.FloatField(max_length = 100, null = True, blank = True,
            verbose_name = _(u'Longitud'),
            help_text = _(u'Puedes introducir directamente las coordenadas (longitud) si las conoces. Ej. -3.533563'))

    # Contact info
    contact_phone_1 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Teléfono contacto 1'),
            help_text = _(u'Un número de teléfono a quien llamar.'))
    contact_phone_2 = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Teléfono contacto 2'),
            help_text = _(u'Se pueden poner dos teléfonos, ejemplo un fijo y un móvil.'))
    fax = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Fax'),
            help_text = _(u'También se puede poner un número de fax.'))
    email = models.EmailField(null = False, blank = True, default = '',
            verbose_name = _(u'Email 1'),
            help_text = _(u'Email de contacto. Ojo: poner la dirección correcta y sin añadir espacios a izquierda ni derecha. Ej. colectivo@gmail.com'))
    email_2 = models.EmailField(null = False, blank = True, default = '',
            verbose_name = _(u'Email 2'),
            help_text = _(u'Se puede poner un segundo email de contacto.'))
    web = models.URLField(null = False, blank = True, default = '',
            verbose_name = _(u'Web 1'),
            help_text = _(u'Página web informativa. Ojo: hay que poner la dirección completa, incluyendo http://. La dirección será validada automáticamente para comprobar que existe.'))
    web_2 = models.URLField(null = False, blank = True, default = '',
            verbose_name = _(u'Web 2'),
            help_text = _(u'Se puede poner una segunda página web.'))
    contact_person = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Persona contacto'),
            help_text = _(u'Nombre de al menos una persona por quien preguntar.'))

    # Detailed descriptive info
    creation_year = models.IntegerField(null = True, blank = True,
            verbose_name = _(u'Año creación'),
            help_text = _(u'Año en que el colectivo u organización comenzó su actividad (introducir un nº con las cuatro cifras).'))
    legal_form = models.CharField(max_length = 100, null = False, blank = True, default = '',
            verbose_name = _(u'Forma jurídica'),
            help_text = _(u'Con qué forma jurídica concreta está registrada la entidad, si lo está.'))
    description = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Descripción'),
            help_text = _(u'Aquí se puede poner una descripción general, o cualquier cosa que no entre en las casillas siguientes. Si hay poca información, puede ser suficiente con rellenar esta casilla. Alternativamente, puede no ser necesaria si se han rellenado las otras con mucha información.'))
    goals = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Objetivo como entidad'),
            help_text = _(u'Objetivos principales de la entidad, cuál es su razón de ser; qué ofrece a sus socios, usuarios, clientes o público en general.'))
    finances = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Finanzas'),
            help_text = _(u'Indicar cómo gestiona el dinero (con/sin ánimo de lucro, precios de los productos si vende algo, fuentes de ingresos, modo de financiación...).'))
    social_values = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Valores sociales y medioambientales'),
            help_text = _(u'Justificación de por qué merece estar en este directorio, valores que aporta en función de nuestros criterios de selección, en tanto que relaciones humanas y cuidado del medio ambiente.'))
    how_to_access = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Forma de acceso'),
            help_text = _(u'Cómo acceder a los servicios o funciones de la entidad, horarios y lugar de contacto, condiciones de participación, venta o ditribución.'))
    networks_member = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Redes de las que forma parte'),
            help_text = _(u'Indicar si esta entidad está integrada en algún tipo de redes, grupo o plataforma, junto con otras entidades.'))
    networks_works_with = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Otras entidades con las que colabora'),
            help_text = _(u'Indicar si esta entidad trabaja en colaboración con otras entidades o redes, aún sin formar parte de ellas.'))
    ongoing_projects = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Proyectos en marcha'),
            help_text = _(u'Indicar, si se desea, los proyectos importantes que la entidad lleva a cabo o en los que está involucrada.'))
    needs = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Necesidades'),
            help_text = _(u'Indicar si la entidad tiene actualmente alguna necesidad importante que pudiera ser cubierta por otras entidades o personas externas.'))
    offerings = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Qué ofrece'),
            help_text = _(u'Indicar si esta entidad está en disposición de ofrecer recursos u otros elementos que puedan ser útiles a otras entidades relacionadas o personas externas; posibilidades de colaboración.'))
    additional_info = models.TextField(null = False, blank = True, default = '',
            verbose_name = _(u'Información adicional'),
            help_text = _(u'Cualquier otra información no clasificable en las casillas anteriores.'))

    class Meta:
	ordering = ['-creation_date']
	verbose_name = _(u'propuesta de entidad')
	verbose_name_plural = _(u'propuestas de entidades')

    def __unicode__(self):
        return _(u'Propuesta: %s') % self.name

    def __init__(self, *args, **kwargs):
        super(EntityProposal, self).__init__(*args, **kwargs)
        self._current_status = self.status

    def save(self, update_dates = True, *args, **kwargs):
        datetime_now = datetime.now()
        if update_dates:
            if not self.id:
                self.creation_date = datetime_now
            self.modification_date = datetime_now
        else:
            if self.creation_date == None:         # In any case there must be any dates
                self.creation_date = datetime_now
            if self.modification_date == None:
                self.modification_date = datetime_now
        super(self.__class__, self).save(*args, **kwargs)
        if self.main_subcategory and not (self.main_subcategory in self.subcategories.all()):
            self.subcategories.add(self.main_subcategory)

        if self.status != self._current_status:
            current_status = self._current_status
            self._current_status = self.status
            if current_status == EntityProposal.STATUS_PENDING \
               and self.status == EntityProposal.STATUS_ACCEPTED:
                if not self.existing_entity:
                    self.generate_entity()
                else:
                    self.update_entity()
                self.send_mail_accepted()
            if current_status == EntityProposal.STATUS_PENDING \
               and self.status == EntityProposal.STATUS_REJECTED:
                self.send_mail_rejected()

    @property
    def categories(self):
        return Category.objects.filter(id__in = self.subcategories.values_list('category_id'))

    @property
    def active_categories(self):
        return self.categories.filter(is_active = True)

    @property
    def active_subcategories(self):
        return self.subcategories.filter(is_active = True)

    def load_from_entity(self, entity):
        self.existing_entity = entity
        self.name = entity.name
        slug = entity.slug
        self.alias = entity.alias
        self.summary = entity.summary
        is_container = entity.is_container
        contained_in = entity.contained_in
        self.latitude = entity.latitude
        self.longitude = entity.longitude
        self.address_1 = entity.address_1
        self.address_2 = entity.address_2
        self.zipcode = entity.zipcode
        self.city = entity.city
        self.province = entity.province
        self.country = entity.country
        self.zone = entity.zone
        self.contact_phone_1 = entity.contact_phone_1
        self.contact_phone_2 = entity.contact_phone_2
        self.fax = entity.fax
        self.email = entity.email
        self.email_2 = entity.email_2
        self.web = entity.web
        self.web_2 = entity.web_2
        self.contact_person = entity.contact_person
        self.creation_year = entity.creation_year
        self.legal_form = entity.legal_form
        self.description = entity.description
        self.goals = entity.goals
        self.finances = entity.finances
        self.social_values = entity.social_values
        self.how_to_access = entity.how_to_access
        self.networks_member = entity.networks_member
        self.networks_works_with = entity.networks_works_with
        self.ongoing_projects = entity.ongoing_projects
        self.needs = entity.needs
        self.offerings = entity.offerings
        self.additional_info = entity.additional_info
        self.map_source = entity.map_source
        creation_date = None, # will be autogenerated
        modification_date = None, # will be autogenerated
        self.entity_type = entity.entity_type
        self.main_subcategory = entity.main_subcategory
        self.save()

        for subcat in entity.subcategories.all():
            self.subcategories.add(subcat)

    def generate_entity(self):
        entity = EcozoomEntity.objects.create(
                name = self.name,
                slug = '', # will be auto generated
                alias = self.alias,
                summary = self.summary,
                is_container = False,
                contained_in = None,
                latitude = self.latitude,
                longitude = self.longitude,
                address_1 = self.address_1,
                address_2 = self.address_2,
                zipcode = self.zipcode,
                city = self.city,
                province = self.province,
                country = self.country,
                zone = self.zone,
                contact_phone_1 = self.contact_phone_1,
                contact_phone_2 = self.contact_phone_2,
                fax = self.fax,
                email = self.email,
                email_2 = self.email_2,
                web = self.web,
                web_2 = self.web_2,
                contact_person = self.contact_person,
                creation_year = self.creation_year,
                legal_form = self.legal_form,
                description = self.description,
                goals = self.goals,
                finances = self.finances,
                social_values = self.social_values,
                how_to_access = self.how_to_access,
                networks_member = self.networks_member,
                networks_works_with = self.networks_works_with,
                ongoing_projects = self.ongoing_projects,
                needs = self.needs,
                offerings = self.offerings,
                additional_info = self.additional_info,
                map_source = self.map_source,
                creation_date = None, # will be autogenerated
                modification_date = None, # will be autogenerated
                is_active = True,
                entity_type = self.entity_type,
                main_subcategory = self.main_subcategory,
            )
        for subcat in self.subcategories.all():
            entity.subcategories.add(subcat)
        self.existing_entity = entity
        self.save()
        #task__geolocalize_entity.delay(self.existing_entity.pk)

    def update_entity(self):
        if self.existing_entity.name != self.name:
            self.existing_entity.name = self.name
            self.existing_entity.slug = slugify_uniquely(self.existing_entity.name, self.existing_entity.__class__)
        self.existing_entity.alias = self.alias
        self.existing_entity.summary = self.summary
        self.existing_entity.is_container = False
        self.existing_entity.contained_in = None
        if self.latitude and self.longitude:
            self.existing_entity.latitude = self.latitude
            self.existing_entity.longitude = self.longitude
        self.existing_entity.address_1 = self.address_1
        self.existing_entity.address_2 = self.address_2
        self.existing_entity.zipcode = self.zipcode
        self.existing_entity.city = self.city
        self.existing_entity.province = self.province
        self.existing_entity.country = self.country
        self.existing_entity.zone = self.zone
        self.existing_entity.contact_phone_1 = self.contact_phone_1
        self.existing_entity.contact_phone_2 = self.contact_phone_2
        self.existing_entity.fax = self.fax
        self.existing_entity.email = self.email
        self.existing_entity.email_2 = self.email_2
        self.existing_entity.web = self.web
        self.existing_entity.web_2 = self.web_2
        self.existing_entity.contact_person = self.contact_person
        self.existing_entity.creation_year = self.creation_year
        self.existing_entity.legal_form = self.legal_form
        self.existing_entity.description = self.description
        self.existing_entity.goals = self.goals
        self.existing_entity.finances = self.finances
        self.existing_entity.social_values = self.social_values
        self.existing_entity.how_to_access = self.how_to_access
        self.existing_entity.networks_member = self.networks_member
        self.existing_entity.networks_works_with = self.networks_works_with
        self.existing_entity.ongoing_projects = self.ongoing_projects
        self.existing_entity.needs = self.needs
        self.existing_entity.offerings = self.offerings
        self.existing_entity.additional_info = self.additional_info
        self.existing_entity.map_source = self.map_source
        self.existing_entity.is_active = True
        self.existing_entity.entity_type = self.entity_type
        self.existing_entity.main_subcategory = self.main_subcategory
        self.existing_entity.save()

        self.existing_entity.subcategories.clear()
        for subcat in self.subcategories.all():
            self.existing_entity.subcategories.add(subcat)

    def send_mail_accepted(self):
        self.send_mail(True)

    def send_mail_rejected(self):
        self.send_mail(False)

    def send_mail(self, accepted):
        if self.proponent_email:
            current_site = Site.objects.get_current()
            site_info = current_site.site_info
            if self.existing_entity:
                action = _(u'actualizar')
            else:
                action = _(u'dar de alta')

            if accepted:
                email_subject = _(u'Hemos aceptado tu solicitud para %(action)s %(entity_name)s en %(website_name)s') % {
                    'entity_name': self.name,
                    'action': action,
                    'website_name': site_info.website_name
                }
            else:
                email_subject = _(u'Hemos rechazado tu solicitud para %(action)s %(entity_name)s en %(website_name)s') % {
                    'entity_name': self.name,
                    'action': action,
                    'website_name': site_info.website_name
                }
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = (self.proponent_email,)
            email_context = Context({
                'entity_name': self.name,
                'action': action,
                'status_info': self.status_info,
                'website_name': site_info.website_name,
            })
            if accepted:
                from django.core.urlresolvers import reverse
                email_context.update({
                    'entity_url': 'http://' + current_site.domain +
                                  reverse('base:entity', kwargs={'entity_slug': self.existing_entity.slug})
                })
                email_template = loader.get_template('macadjan_form/email_notify_accept_to_proponent.txt')
            else:
                email_template = loader.get_template('macadjan_form/email_notify_reject_to_proponent.txt')
            email_body = email_template.render(email_context)
            email_obj = EmailMessage(
                from_email=email_from,
                subject=email_subject,
                body=email_body,
                to=email_to,
            )
            email_obj.content_subtype = 'plain'
            email_obj.send()

