import os
from pathlib import Path
import os
import dj_database_url

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: ¡Mantenlo en False en producción!
DEBUG = False

SECRET_KEY = 'django-insecure-n5d*s%&x_8r+gsdotofeen1k8*v98#9xh)e@c=ozb$#fj4h4m5'

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalogo',
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
# Base de datos
# Por defecto usamos SQLite3 en tu compu local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🚀 EL TRUCO PARA RENDER: 
# Si Render nos pasa una "DATABASE_URL" secreta, la usamos y pisamos la anterior
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
LANGUAGE_CODE = 'es-ar' # Cambiado a español
TIME_ZONE = 'America/Argentina/Buenos_Aires' # Ajustado a tu zona
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS Y MEDIA (CLAVE PARA IMÁGENES) ---

# Configuración para CSS, JS, etc.
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración para las fotos de tus productos
MEDIA_URL = '/media/'

# --- CONFIGURACIÓN DE JAZZMIN (DISEÑO DEL ADMIN) ---
JAZZMIN_SETTINGS = {
    "site_title": "Admin Tienda",
    "site_header": "Panel de Control",
    "site_brand": "Tu Tienda",
    "welcome_sign": "¡Bienvenido al panel de control, EmiDios!",
    "copyright": "Desarrollado por devko",
    
    # Menú superior
    "topmenu_links": [
        {"name": "Ver Sitio Web",  "url": "/", "permissions": ["auth.view_user"]},
    ],
    
    # Íconos para el menú lateral (Usa FontAwesome)
    "icons": {
        "catalogo.Producto": "fas fa-tshirt",
        "catalogo.Categoria": "fas fa-tags",
        "catalogo.Talle": "fas fa-ruler-horizontal",
        "catalogo.Pedido": "fas fa-shopping-cart",
        "catalogo.ConfiguracionSitio": "fas fa-cogs",
    },
    
    # ESTO ES CLAVE: Te deja cambiar colores desde la misma web
    "show_ui_builder": True,
}

# Tema por defecto (Oscuro con toques rojos para mantener tu estilo)
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURACIÓN DE IMÁGENES (CLOUDINARY) ---
cloudinary_url = os.environ.get("CLOUDINARY_URL")

if cloudinary_url:
    # Si estamos en Render, guardamos las fotos en la nube
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Si estamos en tu compu, las guardamos en la carpeta local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

