#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# LA LÍNEA MÁGICA: Crea el usuario 'emi' si no existe todavía
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='dekvo').exists() or User.objects.create_superuser('dekvo', 'dekvo@tienda.com', 'Caca4444')"