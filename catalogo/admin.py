from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Columnas que vas a ver en la lista principal
    list_display = ('nombre', 'categoria', 'precio', 'en_oferta')
    
    # Filtros laterales para buscar rápido
    list_filter = ('categoria', 'en_oferta')
    
    # Barra de búsqueda superior
    search_fields = ('nombre', 'descripcion')
    
    # ¡LA MAGIA!: Te deja editar estos campos directo desde la grilla
    list_editable = ('precio', 'en_oferta') 
    
    # Cuántos productos mostrar por página
    list_per_page = 20