# catalogo/admin.py
from django.contrib import admin
from .models import Categoria, Producto, Talle, ConfiguracionSitio, Pedido, DetallePedido

# 1. Registro del ABM de Talles
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
    filter_horizontal = ('talles',) 

# 3. Configuración de Pedidos (Para ver los detalles adentro)
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unitario', 'talle_elegido')
    can_delete = False

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'creado_en', 'nombre', 'apellido', 'total') 
    list_filter = ('creado_en',)
    search_fields = ('nombre', 'apellido', 'telefono')
    inlines = [DetallePedidoInline] # Acá inyectamos los productos adentro del pedido

# 4. Registros simples
admin.site.register(Categoria)
admin.site.register(ConfiguracionSitio)