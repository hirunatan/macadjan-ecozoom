# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.views.generic import RedirectView, TemplateView, FormView, View
from django.contrib.sites.models import Site

from macadjan_ecozoom import models as models_ecozoom
from . import models
from . import forms


class EntityProposal(FormView):
    template_name = 'macadjan_form/entity_proposal.html'
    form_class = forms.EntityProposalForm

    def dispatch(self, request, entity_slug = None, *args, **kwargs):
        if not entity_slug:
            if not Site.objects.get_current().site_info.new_entity_proposal_enabled:
                raise Http404('Entry proposal form is disabled')
        else:
            if not Site.objects.get_current().site_info.entity_change_proposal_enabled:
                raise Http404('Entry change form is disabled')
        self.entity = get_object_or_404(models_ecozoom.EcozoomEntity, slug = entity_slug) if entity_slug else None
        return super(EntityProposal, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EntityProposal, self).get_context_data(**kwargs)
        context.update({
                'entity': self.entity,
            })
        return context

    def get_form_kwargs(self):
        kwargs = super(EntityProposal, self).get_form_kwargs()
        if self.entity:
            instance = models.EntityProposal()
            instance.load_from_entity(self.entity)
            kwargs.update({'instance': instance})
            instance.delete()  # remove from db but still useful to render the form
        return kwargs

    def get_success_url(self):
        if self.entity:
            return reverse('entity-proposal-ok', args=[self.entity.slug])
        else:
            return reverse('entity-proposal-ok')

    def form_valid(self, form):
        proposal = form.save()
        if proposal.existing_entity:
            action = _(u'actualizar')
        else:
            action = _(u'dar de alta')
        self.send_mail_to_managers(proposal, action)
        self.send_mail_to_proponent(proposal, action)
        return super(EntityProposal, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _(u'Ha habido algún error, comprueba los mensajes más abajo.'))
        return super(EntityProposal, self).form_invalid(form)

    def send_mail_to_managers(self, proposal, action):
        current_site = Site.objects.get_current()
        site_info = current_site.site_info

        email_subject = _(u'[%(website_name)s] Se ha recibido una solicitud de %(action)s entidad') %  {
                'website_name': site_info.website_name,
                'action': action
        }
        email_from = settings.DEFAULT_FROM_EMAIL
        email_reply_to = getattr(settings, 'DEFAULT_REPLY_TO_EMAIL', '')
        email_headers = {}
        if email_reply_to:
            email_headers['Reply-To'] = email_reply_to
        email_to = [tuple[1] for tuple in settings.MANAGERS]
        email_template = loader.get_template('macadjan_form/email_notify_proposal_to_managers.txt')
        email_context = Context({
            'entity_name': proposal.name,
            'action': action,
            'sender': (_(u'Dirección del remitente: %s') % proposal.proponent_email)
                       if proposal.proponent_email else _(u'Sin dirección de remitente.'),
            'comment': proposal.proponent_comment
                       if proposal.proponent_comment else _(u'Sin comentarios del remitente.'),
            'link': 'http://' + Site.objects.get_current().domain + \
                    '/admin/macadjan_form/entityproposal/%d/' % proposal.id,
        })
        email_body = email_template.render(email_context)
        email_obj = EmailMessage(
            from_email=email_from,
            subject=email_subject,
            body=email_body,
            to=email_to,
            headers=email_headers,
        )
        email_obj.content_subtype = 'plain'
        email_obj.send()

    def send_mail_to_proponent(self, proposal, action):
        if proposal.proponent_email:

            current_site = Site.objects.get_current()
            site_info = current_site.site_info

            email_subject = _(u'Hemos recibido tu solicitud para %(action)s %(entity_name)s en %(website_name)s') % {
                'entity_name': proposal.name,
                'action': action,
                'website_name': site_info.website_name
            }
            email_from = settings.DEFAULT_FROM_EMAIL
            email_headers = {}
            email_reply_to = getattr(settings, 'DEFAULT_REPLY_TO_EMAIL', '')
            if email_reply_to:
                email_headers['Reply-To'] = email_reply_to
            email_to = (proposal.proponent_email,)
            email_template = loader.get_template('macadjan_form/email_notify_proposal_to_proponent.txt')
            email_context = Context({
                'entity_name': proposal.name,
                'action': action,
                'website_name': site_info.website_name,
            })
            email_body = email_template.render(email_context)
            email_obj = EmailMessage(
                from_email=email_from,
                subject=email_subject,
                body=email_body,
                to=email_to,
                headers=email_headers,
            )
            email_obj.content_subtype = 'plain'
            email_obj.send()


class EntityProposalOk(TemplateView):
    template_name = 'macadjan_form/entity_proposal_ok.html'

    def dispatch(self, request, entity_slug = None, *args, **kwargs):
        if not entity_slug:
            if not Site.objects.get_current().site_info.new_entity_proposal_enabled:
                raise Http404('Entry proposal form is disabled')
        else:
            if not Site.objects.get_current().site_info.entity_change_proposal_enabled:
                raise Http404('Entry change form is disabled')
        self.entity = get_object_or_404(models_ecozoom.EcozoomEntity, slug = entity_slug) if entity_slug else None
        return super(EntityProposalOk, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EntityProposalOk, self).get_context_data(**kwargs)
        context.update({
                'entity': self.entity,
            })
        return context

