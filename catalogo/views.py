# catalogo/views.py
import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Pedido, DetallePedido, ConfiguracionSitio
from .carrito import Carrito 
from .forms import PedidoForm

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
    
    # Si el carrito está vacío, lo mandamos al inicio
    if not carrito.carrito:
        return redirect('inicio')

    # Si el cliente ya completó el formulario y tocó "Finalizar Pedido"
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            
            # 1. Guardamos los datos del cliente y el total
            pedido = form.save(commit=False)
            total_pedido = carrito.obtener_total_precio()
            pedido.total = float(total_pedido)
            pedido.save() # Guardamos en la base de datos

            # 2. Armamos el mensaje para WhatsApp (Ahora sumamos los datos del cliente)
            mensaje_wa = f"¡Hola! 👋 Quiero confirmar mi Pedido #{pedido.id}:\n"
            mensaje_wa += f"👤 Nombre: {pedido.nombre} {pedido.apellido}\n"
            mensaje_wa += f"📞 Teléfono: {pedido.telefono}\n"
            if pedido.direccion:
                mensaje_wa += f"📍 Dirección: {pedido.direccion}\n"
            mensaje_wa += "\n🛒 *Mis Productos:*\n"

            # 3. Guardamos los detalles (los talles) y sumamos al mensaje
            for key, value in carrito.carrito.items():
                producto = Producto.objects.get(id=value['producto_id'])
                talle_texto = value.get('talle') 
                
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=value['cantidad'],
                    precio_unitario=producto.precio,
                    talle_elegido=talle_texto
                )
                
                str_talle = f" (Talle: {talle_texto})" if talle_texto else ""
                mensaje_wa += f"🔸 {value['cantidad']}x {value['nombre']}{str_talle} (${value['acumulado']})\n"

            mensaje_wa += f"\n*TOTAL: ${total_pedido}*\n\n¡Gracias!"

            # 4. Vaciar el carrito
            carrito.limpiar()

            # 5. Buscar el número de teléfono en la configuración
            try:
                conf = ConfiguracionSitio.objects.get(pk=1)
                numero_wa = conf.whatsapp.replace('+', '').replace(' ', '') if conf.whatsapp else ""
            except ConfiguracionSitio.DoesNotExist:
                numero_wa = ""

            # 6. Redirigir a WhatsApp (¡Esta es la línea esencial que faltaba!)
            if numero_wa:
                mensaje_codificado = urllib.parse.quote(mensaje_wa)
                return redirect(f"https://wa.me/{numero_wa}?text={mensaje_codificado}")
            else:
                return redirect('inicio')
                
    # Si el cliente recién entra desde el carrito, le mostramos el formulario vacío
    else:
        form = PedidoForm()

    # Le escupimos el HTML del formulario que armamos antes
    return render(request, "catalogo/checkout.html", {"form": form})