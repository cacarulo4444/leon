# catalogo/carrito.py
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    # ACÁ ESTÁ EL CAMBIO: agregamos ", cantidad=1"
    def agregar(self, producto, cantidad=1):
        id = str(producto.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                # Multiplicamos el precio por la cantidad que elegiste
                "acumulado": float(producto.precio) * int(cantidad),
                "cantidad": int(cantidad),
            }
        else:
            # Si ya estaba, sumamos la nueva cantidad a la anterior
            self.carrito[id]["cantidad"] += int(cantidad)
            self.carrito[id]["acumulado"] += float(producto.precio) * int(cantidad)
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def obtener_total_unidades(self):
        # Sumamos el valor del campo 'cantidad' de cada item en el carrito
        return sum(item['cantidad'] for item in self.carrito.values())
    
    def obtener_total_precio(self):
        # Sumamos el campo 'acumulado' de cada producto en el carrito
        return sum(item['acumulado'] for item in self.carrito.values())
    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True