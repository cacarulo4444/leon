import os
import django

# Le avisamos a Django cuál es tu archivo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

from django.contrib.auth.models import User

# Le decimos: "Si el usuario emidios no existe, crealo"
if not User.objects.filter(username='emidios').exists():
    # Parámetros: Usuario, Email, Contraseña (¡poné la que vos quieras acá!)
    User.objects.create_superuser('cacarulo4444', 'emi@emi.com', 'Caca44')
    print("¡Administrador creado con éxito!")