import os
import dj_database_url
import locale


os.environ["LANG"] = "es_CO.UTF-8"
os.environ["LC_ALL"] = "es_CO.UTF-8"

try:
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

# Build paths inside the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'cambia-esto-por-una-clave-segura')
# DEBUG = os.getenv('DEBUG', 'False') == 'True'
DEBUG = True

PORT = os.getenv("PORT", "8000")
ALLOWED_HOSTS = ["*"]




# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'widget_tweaks',
    'core.erp',
    'core.homepage',
    'core.login',
    'core.user',
    'core.reports',
]

# Middleware
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'enfokart',  # Usa el nombre de tu base de datos
        'USER': 'enfokart_user',  # Usa el nombre de usuario
        'PASSWORD': 'MxNjNgXOpSHZoyz0q4uYxeiIN36griQM',  # Usa la contraseña proporcionada
        'HOST': 'dpg-cvb2dflrie7s739b6oq0-a.oregon-postgres.render.com',  # El host de tu base de datos
        'PORT': '5432',  # Puerto estándar de PostgreSQL
        'OPTIONS': {
            'sslmode': 'require',  # Asegúrate de que la conexión sea SSL
        }
    }
}




ROOT_URLCONF = 'config.urls'


PORT = os.getenv('PORT', '10000')  # Render detectó el puerto 10000
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


# Templates
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

# WSGI application
WSGI_APPLICATION = 'config.wsgi.application'

# Authentication
AUTH_USER_MODEL = 'user.User'
LOGIN_REDIRECT_URL = '/erp/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'es-CO'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'erp','static'),  # Si tu carpeta de estáticos está en otro lugar, ajústalo
]




# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sessions
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'





