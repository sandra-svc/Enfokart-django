import os
import locale

# Intenta establecer un locale compatible con Babel
try:
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')  # o 'en_US.UTF-8' si prefieres inglés
except locale.Error:
    print("No se pudo establecer 'es_CO.UTF-8', intentando con 'C.UTF-8'")
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except locale.Error:
        print("No se pudo establecer ningún locale completo, el formato de moneda puede fallar")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()

