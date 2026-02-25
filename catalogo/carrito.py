# catalogo/carrito.py
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1, talle=None):
        # Generamos una clave única: "ID-Talle" o solo "ID"
        clave = str(producto.id)
        if talle:
            clave += f"-{talle}"

        if clave not in self.carrito.keys():
            self.carrito[clave] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "acumulado": float(producto.precio) * int(cantidad),
                "cantidad": int(cantidad),
                "talle": talle, # ¡Guardamos el talle en la memoria!
            }
        else:
            # Si ya estaba este producto con este mismo talle, sumamos cantidad
            self.carrito[clave]["cantidad"] += int(cantidad)
            self.carrito[clave]["acumulado"] += float(producto.precio) * int(cantidad)
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def obtener_total_unidades(self):
        return sum(item['cantidad'] for item in self.carrito.values())
    
    def obtener_total_precio(self):
        return sum(item['acumulado'] for item in self.carrito.values())

    # Modificamos eliminar para que reciba la 'clave' (ej: 4-M) y no el producto entero
    def eliminar(self, clave):
        clave_str = str(clave)
        if clave_str in self.carrito:
            del self.carrito[clave_str]
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True