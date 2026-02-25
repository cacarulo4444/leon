import os
from django.db import models

# 1. FUNCIÓN PARA RUTAS DINÁMICAS (Arreglada para no crear subcarpetas)
def ruta_dinamica_categoria(instance, filename):
    # Retorna SOLO el nombre del archivo para que Django lo guarde directo en MEDIA_ROOT
    return filename

# 2. MODELO CATEGORIA
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# 3. MODELO TALLE (Definido AQUÍ arriba para que Producto lo reconozca)
class Talle(models.Model):
    nombre = models.CharField(max_length=50, help_text="Ej: S, M, L o 42, 44")

    def __str__(self):
        return self.nombre

# 4. MODELO PRODUCTO
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Relación con categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    
    # Relación con talles (Muchos a Muchos)
    talles = models.ManyToManyField(Talle, blank=True, help_text="Seleccioná los talles disponibles")
    
    # Imagen con la ruta corregida
    imagen = models.ImageField(upload_to=ruta_dinamica_categoria, null=True, blank=True)
    
    # Campo para Ofertas
    en_oferta = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

# 5. CONFIGURACIÓN DEL SITIO
class ConfiguracionSitio(models.Model):
    nombre_empresa = models.CharField(
        max_length=100, 
        default="TU MARCA", 
        help_text="Nombre que se mostrará en el encabezado."
    )
    whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: +5491123456789")
    email = models.EmailField(blank=True, null=True, help_text="Ej: ventas@tumarca.com")
    texto_informacion = models.TextField(blank=True, null=True, help_text="Info de envíos, talles, etc.")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(ConfiguracionSitio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"

# 6. MODELOS DE PEDIDOS
class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    # Agregamos campo de talle al detalle para que quede registrado qué talle compraron
    talle_elegido = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Eliminado'} ({self.talle_elegido})"