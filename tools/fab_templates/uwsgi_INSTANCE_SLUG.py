import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.%(instance_slug)s_pro'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

