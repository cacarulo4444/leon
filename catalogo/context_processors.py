# catalogo/context_processors.py
from .models import ConfiguracionSitio

def datos_empresa(request):
    try:
        # Busca la configuración (siempre es la ID 1 por cómo lo armamos)
        conf = ConfiguracionSitio.objects.get(pk=1)
        return {
            'nombre_empresa': conf.nombre_empresa,
            'whatsapp_empresa': conf.whatsapp,
            'email_empresa': conf.email,
            'info_empresa': conf.texto_informacion
        }
    except ConfiguracionSitio.DoesNotExist:
        # Por si te olvidás de crearlo en el admin, no se rompe nada
        return {
            'nombre_empresa': "TU MARCA",
            'whatsapp_empresa': "",
            'email_empresa': "",
            'info_empresa': ""
        }