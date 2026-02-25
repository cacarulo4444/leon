from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from catalogo import views  # <--- Importamos tus vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'), 
    
    # --- RUTAS NUEVAS DE LAS PESTAÑAS ---
    path('ofertas/', views.ofertas, name='ofertas'),
    path('contacto/', views.contacto, name='contacto'),
    path('informacion/', views.informacion, name='informacion'),

    path('producto/<int:producto_id>/', views.detalle, name='detalle'),
    
    # --- RUTAS DEL CARRITO ---
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    
    # ACÁ ESTÁ EL CAMBIO IMPORTANTE PARA BORRAR PRODUCTOS
    path('eliminar/<str:clave>/', views.eliminar_del_carrito, name='eliminar'),
    
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)