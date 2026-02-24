# catalogo/admin.py
from django.contrib import admin
from .models import Categoria, Producto, Talle, ConfiguracionSitio, Pedido, DetallePedido

# 1. Registro de Talles (ABM simple)
@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

# 2. Configuración de Productos (Con buscador de talles)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'en_oferta')
    list_filter = ('categoria', 'en_oferta')
    search_fields = ('nombre',)
    # Esto hace que elegir talles sea mucho más fácil:
    filter_horizontal = ('talles',) 

# 3. Configuración de Pedidos (Para ver los detalles adentro)
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unitario', 'talle_elegido')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'total')
    list_filter = ('fecha',)
    inlines = [DetallePedidoInline]

# 4. Registros simples restantes
admin.site.register(Categoria)
admin.site.register(ConfiguracionSitio)