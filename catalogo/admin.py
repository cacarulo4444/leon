# catalogo/admin.py
from django.contrib import admin
from .models import Categoria, Producto, Talle, ConfiguracionSitio, Pedido, DetallePedido


admin.site.register(Talle)
# Esto hace que veas los productos adentro del mismo pedido
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'total')
    inlines = [DetallePedidoInline]

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Talle)
admin.site.register(ConfiguracionSitio)
admin.site.register(Pedido, PedidoAdmin) 