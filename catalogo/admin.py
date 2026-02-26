from django.contrib import admin
# IMPORTANTE: Asegurate de que DetallePedido sea el nombre correcto de tu tabla en models.py
from .models import Categoria, Producto, Pedido, Talle, ConfiguracionSitio, DetallePedido 

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',) # Le agregamos buscador a los talles por las dudas

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'en_oferta')
    list_filter = ('categoria', 'en_oferta')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'en_oferta') 
    
    # Buscador predictivo para categoría
    autocomplete_fields = ['categoria'] 
    
    # ¡LA MAGIA DE LOS TALLES!: Crea dos columnas limpias para pasar talles de un lado a otro.
    # (Asumo que en tu models.py el campo de la relación se llama 'talles')
    filter_horizontal = ('talles',) 
    
    list_per_page = 20

# --- TABLITA INTERNA DE PRODUCTOS PARA EL PEDIDO ---
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido  # <-- Ajustá este nombre si tu modelo se llama distinto
    extra = 0

# --- PANTALLA PRINCIPAL DE PEDIDOS ---
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'direccion', 'total')
    search_fields = ('nombre', 'apellido', 'telefono')
    
    # Inyectamos los productos adentro de la ficha del pedido
    inlines = [DetallePedidoInline]

# Configuraciones extra
admin.site.register(ConfiguracionSitio)