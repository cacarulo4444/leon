import os
from django.db import models

# Función para organizar las fotos en subcarpetas por categoría
def ruta_dinamica_categoria(instance, filename):
    categoria_nombre = instance.categoria.nombre if instance.categoria else 'sin_categoria'
    # QUITAMOS 'productos' de aquí abajo:
    return os.path.join(categoria_nombre, filename)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Relación con categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    
    # Usamos la función de ruta dinámica aquí
    imagen = models.ImageField(upload_to=ruta_dinamica_categoria, null=True, blank=True)
    
    # Campo clave para la pestaña de OFERTAS
    en_oferta = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class ConfiguracionSitio(models.Model):
    nombre_empresa = models.CharField(
        max_length=100, 
        default="TU MARCA", 
        help_text="Nombre que se mostrará en el encabezado con tipografía urbana."
    )
    # --- NUEVOS CAMPOS DE CONTACTO E INFO ---
    whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: +5491123456789")
    email = models.EmailField(blank=True, null=True, help_text="Ej: ventas@tumarca.com")
    texto_informacion = models.TextField(blank=True, null=True, help_text="Detalles de talles, envíos, etc. (Podés usar Enter para separar párrafos)")

    def save(self, *args, **kwargs):
        # Esto asegura que solo exista UN registro de configuración.
        # Si tratas de crear otro, sobrescribe el primero.
        self.pk = 1
        super(ConfiguracionSitio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"
    # catalogo/models.py (al final del archivo)

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

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto Eliminado'}"