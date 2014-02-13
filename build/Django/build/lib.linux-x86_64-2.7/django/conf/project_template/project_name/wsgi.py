"""
WSGI config for {{ invoice4django }} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ invoice4django }}.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
