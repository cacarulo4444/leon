# catalogo/admin.py
from django.contrib import admin
# AGREGAMOS 'Talle' a la importación
from .models import Categoria, Producto, Talle, ConfiguracionSitio, Pedido, DetallePedido

# 1. Registro del ABM de Talles (¡ESTO ES LO QUE TE FALTA!)
@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

# 2. Registro de Productos con selector de talles pro
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'en_oferta')
    list_filter = ('categoria', 'en_oferta')
    search_fields = ('nombre',)
    # Esto crea el selector horizontal para los talles que agregamos al modelo
    filter_horizontal = ('talles',) 

# 3. Configuración de Pedidos (Para ver los detalles adentro)
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    # Agregamos talle_elegido para que lo veas en el pedido de venta
    readonly_fields = ('producto', 'cantidad', 'precio_unitario', 'talle_elegido')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Cambiamos 'fecha' por 'creado_en' para que coincida con el modelo
    list_display = ('id', 'creado_en', 'nombre', 'apellido', 'total') 
    list_filter = ('creado_en',)

# 4. Registros simples
admin.site.register(Categoria)
admin.site.register(ConfiguracionSitio)