import os
from pathlib import Path
import dj_database_url

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: ¡Mantenlo en False en producción!
DEBUG = True

SECRET_KEY = 'django-insecure-n5d*s%&x_8r+gsdotofeen1k8*v98#9xh)e@c=ozb$#fj4h4m5'

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost', '.onrender.com']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'catalogo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configuracion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catalogo.context_processors.datos_empresa',
            ],
        },
    },
]

WSGI_APPLICATION = 'configuracion.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🚀 EL TRUCO PARA RENDER: 
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES['default'] = dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es-ar' 
TIME_ZONE = 'America/Argentina/Buenos_Aires' 
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS Y MEDIA ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ESTA LÍNEA PERMITE AGREGAR TUS PROPIOS DISEÑOS CSS:
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'

# --- CONFIGURACIÓN DE JAZZMIN (DISEÑO DEL ADMIN) ---
JAZZMIN_SETTINGS = {
    "site_title": "Admin Tienda",
    "site_header": "Panel de Control",
    "site_brand": "Tu Tienda",
    "welcome_sign": "¡Bienvenido al panel de control!",
    "copyright": "Desarrollado por devko",
    
    # Menú superior
    "topmenu_links": [
        {"name": "Ver Sitio Web",  "url": "/", "permissions": ["auth.view_user"]},
    ],
    
    # Íconos para el menú lateral
    "icons": {
        "catalogo.Producto": "fas fa-tshirt",
        "catalogo.Categoria": "fas fa-tags",
        "catalogo.Talle": "fas fa-ruler-horizontal",
        "catalogo.Pedido": "fas fa-shopping-cart",
        "catalogo.ConfiguracionSitio": "fas fa-cogs",
    },
    
    "show_ui_builder": True,
    # ESTA LÍNEA CONECTA TU PARCHE DE LETRAS NEGRAS:
    "custom_css": "css/admin_fix.css",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURACIÓN DE IMÁGENES (CLOUDINARY) ---
cloudinary_url = os.environ.get("CLOUDINARY_URL")

if cloudinary_url:
    # Para versiones nuevas de Django (Django 4.2 y 5+) en Render
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    # Si estamos en tu compu, las guardamos en la carpeta local
    MEDIA_ROOT = BASE_DIR / 'media'