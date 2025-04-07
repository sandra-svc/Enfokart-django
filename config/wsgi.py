"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import locale

# Intentamos establecer un locale compatible
try:
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'C')  # Fallback si 'C.UTF-8' no está disponible

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
