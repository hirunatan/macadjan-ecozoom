from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
from django.conf import settings
from django.contrib.sites.models import Site

class Command(BaseCommand):
    args = '<new_domain>'
    help = 'Change the domain of the instance in the Site object.\n' \
           'You need to give the new domain. For example:\n' \
           '  ./manage.py change_domain_instance newdemo.mapunto.net'

    def handle(self, *args, **options):

        if len(args) != 1:
           return 'You need to give the new domain. For example:\n' \
                  '  ./manage.py change_domain_instance newdemo.mapunto.net\n'

        new_domain = args[0]

        translation.activate(settings.LANGUAGE_CODE)

        current_site = Site.objects.get_current()
        current_site.name = new_domain
        current_site.domain = new_domain
        current_site.save()

        translation.deactivate()

        print 'Changed domain to %s' % new_domain
