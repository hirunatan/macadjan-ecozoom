# -*- coding: utf-8 -*-

# Those decorators are prepared to be attached to 'dispatch' methods of View
# classes, by adding a 'self' parameter. So, it's no longer necessary to use
# method_decorator, as explained in:
# https://docs.djangoproject.com/en/1.3/topics/class-based-views/#decorating-the-class

from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from django.template import RequestContext

def staff_required():
    '''
    Decorator to check that the user is authenticated and has 'is_staff' status.
    '''
    def _dec(view_func):
        def _check_user(self, request, *args, **kwargs):
            if request.user.is_staff:
                return view_func(self, request, *args, **kwargs)
            else:
                return HttpResponseForbidden(render_to_string('403.html',
                    context_instance=RequestContext(request)))

        return _check_user

    return _dec

