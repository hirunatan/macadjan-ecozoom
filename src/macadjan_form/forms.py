# -*- coding: utf-8 -*-

from django import forms
from django.forms import formsets
from captcha.fields import CaptchaField
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from . import models

class EntityProposalForm(forms.ModelForm):

    captcha = CaptchaField(
        label = _(u'Clave de seguridad'),
        help_text = _(u'Introduce el texto que ves en la imagen (esto es para evitar spam).')
    )

    class Meta:
        model = models.EntityProposal
        exclude = ('existing_entity', 'status', 'status_info', 'internal_comment', 'creation_date', 'modification_date', 'map_source')

    def __init__(self, *args, **kwargs):
        super(EntityProposalForm, self).__init__(*args, **kwargs)
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
        except models.SiteInfo.DoesNotExist:
            return {}

