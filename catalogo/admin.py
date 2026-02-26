from django.contrib import admin
from .models import Categoria, Producto, Pedido, Talle, ConfiguracionSitio

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    # ESTO ES VITAL: Le dice a Django por qué campo buscar cuando tipeás
    search_fields = ('nombre',) 

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'en_oferta')
    list_filter = ('categoria', 'en_oferta')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'en_oferta') 
    
    # LA MAGIA PREDICTIVA: Convierte el desplegable en un buscador con autocompletado
    autocomplete_fields = ['categoria'] 
    
    list_per_page = 20

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Asumiendo los campos clásicos de un pedido (ajustalo si tus campos se llaman distinto)
    # list_display = ('id', 'fecha', 'total', 'estado') 
    # list_filter = ('estado', 'fecha')
    # search_fields = ('id', 'email_cliente')
    pass # Dejalo así por ahora si no tocamos tu modelo de Pedidos todavía

admin.site.register(Talle)
admin.site.register(ConfiguracionSitio)