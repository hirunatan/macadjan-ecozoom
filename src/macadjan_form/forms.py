# -*- coding: utf-8 -*-

from django import forms
from django.forms import formsets
from captcha.fields import CaptchaField
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from . import models
from macadjan.models import SiteInfo

class EntityProposalForm(forms.ModelForm):

    captcha = CaptchaField(
        label = _(u'Clave de seguridad'),
        help_text = _(u'Introduce el texto que ves en la imagen (esto es para evitar spam).')
    )

    class Meta:
        model = models.EntityProposal
        exclude = ('existing_entity', 'status', 'status_info', 'internal_comment', 'creation_date', 
                   'modification_date', 'map_source')

    def __init__(self, *args, **kwargs):
        super(EntityProposalForm, self).__init__(*args, **kwargs)
        for field in self.get_excluded_fields():
            del self.fields[field]
        hints = self.get_current_hints()
        for name, field in self.fields.items():
            field.hints = hints.get(name, u'')
       
    def get_current_hints(self):
        current_site = Site.objects.get_current()
        try:
            site_info = current_site.site_info
            return {
                "description": site_info.description_hints,
                "goals": site_info.goals_hints,
                "finances": site_info.finances_hints,
                "social_values": site_info.social_values_hints,
                "how_to_access": site_info.how_to_access_hints,
                "networks_member": site_info.networks_member_hints,
                "networks_works_with": site_info.networks_works_with_hints,
                "ongoing_projects": site_info.ongoing_projects_hints,
                "needs": site_info.needs_hints,
                "offerings": site_info.offerings_hints,
                "additional_info": site_info.additional_info_hints,
            }
        except SiteInfo.DoesNotExist:
            return {}

    def get_excluded_fields(self):
        current_site = Site.objects.get_current()
        excluded_fields = []
        try:
            site_info = current_site.site_info
            if not site_info.proponent_email_field_enabled: excluded_fields.append('proponent_email')
            if not site_info.proponent_comment_field_enabled: excluded_fields.append('proponent_comment')
            if not site_info.alias_field_enabled: excluded_fields.append('alias')
            if not site_info.summary_field_enabled: excluded_fields.append('summary')
            if not site_info.subcategories_field_enabled: excluded_fields.append('subcategories')
            if not site_info.address_1_field_enabled: excluded_fields.append('.address_1')
            if not site_info.address_2_field_enabled: excluded_fields.append('address_2')
            if not site_info.zipcode_field_enabled: excluded_fields.append('zipcode')
            if not site_info.city_field_enabled: excluded_fields.append('city')
            if not site_info.province_field_enabled: excluded_fields.append('province')
            if not site_info.country_field_enabled: excluded_fields.append('country')
            if not site_info.zone_field_enabled: excluded_fields.append('zone')
            if not site_info.latitude_field_enabled: excluded_fields.append('latitude')
            if not site_info.longitude_field_enabled: excluded_fields.append('longitude')
            if not site_info.contact_phone_1_field_enabled: excluded_fields.append('contact_phone_1')
            if not site_info.contact_phone_2_field_enabled: excluded_fields.append('contact_phone_2')
            if not site_info.fax_field_enabled: excluded_fields.append('fax')
            if not site_info.email_field_enabled: excluded_fields.append('email')
            if not site_info.email_2_field_enabled: excluded_fields.append('email_2')
            if not site_info.web_field_enabled: excluded_fields.append('web')
            if not site_info.web_2_field_enabled: excluded_fields.append('web_2')
            if not site_info.contact_person_field_enabled: excluded_fields.append('contact_person')
            if not site_info.creation_year_field_enabled: excluded_fields.append('creation_year')
            if not site_info.legal_form_field_enabled: excluded_fields.append('legal_form')
            if not site_info.description_field_enabled: excluded_fields.append('description')
            if not site_info.goals_field_enabled: excluded_fields.append('goals')
            if not site_info.finances_field_enabled: excluded_fields.append('finances')
            if not site_info.social_values_field_enabled: excluded_fields.append('social_values')
            if not site_info.how_to_access_field_enabled: excluded_fields.append('how_to_access')
            if not site_info.networks_member_field_enabled: excluded_fields.append('networks_member')
            if not site_info.networks_works_with_field_enabled: excluded_fields.append('networks_works_with')
            if not site_info.ongoing_projects_field_enabled: excluded_fields.append('ongoing_projects')
            if not site_info.needs_field_enabled: excluded_fields.append('needs')
            if not site_info.offerings_field_enabled: excluded_fields.append('offerings')
            if not site_info.additional_info_field_enabled: excluded_fields.append('additional_info')
            return excluded_fields
        except SiteInfo.DoesNotExist:
            return {}
