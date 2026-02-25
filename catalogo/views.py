# catalogo/views.py
import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Pedido, DetallePedido, ConfiguracionSitio
from .carrito import Carrito 

def inicio(request):
    carrito = Carrito(request)
    total_unidades = carrito.obtener_total_unidades()

    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    orden = request.GET.get('orden')
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre':
        productos = productos.order_by('nombre')

    context = {
        'productos': productos, 
        'categorias': categorias,
        'total_unidades': total_unidades
    }
    return render(request, 'catalogo/inicio.html', context)

def detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'catalogo/detalle.html', {'producto': producto})

def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        cantidad = request.POST.get("cantidad", 1)
        talle = request.POST.get("talle") # Atrapamos el talle del HTML

        # 🔒 EL CANDADO DE PYTHON: 
        # Si el producto tiene talles en la base de datos, PERO el cliente no eligió ninguno
        if producto.talles.exists() and not talle:
            # Lo devolvemos a la misma página para que lo elija sí o sí
            return redirect('detalle', producto_id=producto.id)

        carrito.agregar(producto, cantidad=int(cantidad), talle=talle)
    else:
        carrito.agregar(producto)
        
    return redirect("inicio")

def ver_carrito(request):
    carrito = Carrito(request)
    total_precio = carrito.obtener_total_precio()
    
    context = {
        'total_precio': total_precio
    }
    return render(request, 'catalogo/carrito.html', context)

def eliminar_del_carrito(request, clave):
    carrito = Carrito(request)
    carrito.eliminar(clave)
    return redirect("ver_carrito") 

def ofertas(request):
    carrito = Carrito(request)
    total_unidades = carrito.obtener_total_unidades()
    categorias = Categoria.objects.all()
    
    productos = Producto.objects.filter(en_oferta=True)

    orden = request.GET.get('orden')
    if orden == 'precio_asc': productos = productos.order_by('precio')
    elif orden == 'precio_desc': productos = productos.order_by('-precio')
    elif orden == 'nombre': productos = productos.order_by('nombre')

    return render(request, 'catalogo/inicio.html', {
        'productos': productos, 
        'categorias': categorias,
        'total_unidades': total_unidades
    })

def contacto(request):
    carrito = Carrito(request)
    total_unidades = carrito.obtener_total_unidades()
    return render(request, 'catalogo/contacto.html', {'total_unidades': total_unidades})

def informacion(request):
    carrito = Carrito(request)
    total_unidades = carrito.obtener_total_unidades()
    return render(request, 'catalogo/informacion.html', {'total_unidades': total_unidades})

def procesar_pedido(request):
    carrito = Carrito(request)
    if not carrito.carrito:
        return redirect('inicio') # Si está vacío, lo manda al inicio

    # 1. Crear el Pedido en la Base de Datos
    total_pedido = carrito.obtener_total_precio()
    pedido = Pedido.objects.create(total=total_pedido)

    # 2. Armar el mensaje para WhatsApp y guardar los detalles
    mensaje_wa = f"¡Hola! 👋 Quiero confirmar mi Pedido #{pedido.id}:\n\n"

    for key, value in carrito.carrito.items():
        producto = Producto.objects.get(id=value['producto_id'])
        talle_texto = value.get('talle') # Obtenemos el talle guardado
        
        # Guardamos en la base de datos
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=value['cantidad'],
            precio_unitario=producto.precio,
            talle_elegido=talle_texto
        )
        
        # Sumamos al texto de WhatsApp
        str_talle = f" (Talle: {talle_texto})" if talle_texto else ""
        mensaje_wa += f"🔸 {value['cantidad']}x {value['nombre']}{str_talle} (${value['acumulado']})\n"

    mensaje_wa += f"\n*TOTAL: ${total_pedido}*\n\n¡Gracias!"

    # 3. Vaciar el carrito
    carrito.limpiar()

    # 4. Obtener el número de WhatsApp de la configuración
    try:
        conf = ConfiguracionSitio.objects.get(pk=1)
        # Limpiamos el número por si le pusiste espacios o el '+'
        numero_wa = conf.whatsapp.replace('+', '').replace(' ', '') if conf.whatsapp else ""
    except ConfiguracionSitio.DoesNotExist:
        numero_wa = ""

    # 5. Redirigir a WhatsApp
    if numero_wa:
        mensaje_codificado = urllib.parse.quote(mensaje_wa)
        return redirect(f"https://wa.me/{numero_wa}?text={mensaje_codificado}")
    else:
        # Si te olvidaste de cargar el número en el ABM, lo devuelve al inicio
        return redirect('inicio')