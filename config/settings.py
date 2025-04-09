import os
import locale
import dj_database_url

# 🏠 Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔐 Seguridad
SECRET_KEY = os.getenv('SECRET_KEY', 'cambia-esto-por-una-clave-segura')
DEBUG = True  # Cambiar a False en producción
ALLOWED_HOSTS = ["*"]

# 📦 Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'babel',
    'widget_tweaks',
    'core.erp',
    'core.homepage',
    'core.login',
    'core.user',
    'core.reports',
]

# 🛡 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

# 🗄 Base de datos (Render PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'enfokart',
        'USER': 'enfokart_user',
        'PASSWORD': 'MxNjNgXOpSHZoyz0q4uYxeiIN36griQM',
        'HOST': 'dpg-cvb2dflrie7s739b6oq0-a.oregon-postgres.render.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# 🔥 Configuración de Django
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# 🌍 Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es_CO'  # ⚠️ IMPORTANTE: Guion bajo (_), no guion (-)
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = False  # ❌ Desactivar porque Django ya maneja localización
USE_TZ = True

# Configuración de formato numérico
DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3

# 🎨 Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🛡 Seguridad en autenticación
AUTH_USER_MODEL = 'user.User'
LOGIN_REDIRECT_URL = '/erp/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

# 🔑 Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🖼 Archivos estáticos y medios
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'erp', 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# 📧 Configuración de correo
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# 🔑 ID primario automático
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 💾 Configuración de sesiones
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'





