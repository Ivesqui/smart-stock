from datetime import datetime

class Producto:

    def __init__(
        self,
        sku: str,
        nombre_producto: str,
        categoria: str,
        unidad: str,
        precio_compra: float,
        precio_venta: float,
        stock_actual: int,
        stock_minimo: int,
        descripcion: str = "",
        activo: bool = True,
        codigo_barras: str = None,
        fecha_creacion: str = None,
        fecha_actualizacion: str = None
    ):

        if not sku or not sku.strip():
            raise ValueError("El SKU no puede estar vacío")

        if precio_venta < precio_compra:
            raise ValueError("El precio de venta no puede ser menor al de compra")

        self.__sku = sku
        self.__nombre_producto = nombre_producto
        self.__categoria = categoria
        self.__descripcion = descripcion
        self.__unidad = unidad
        self.__precio_compra = precio_compra
        self.__precio_venta = precio_venta
        self.__stock_actual = stock_actual
        self.__stock_minimo = stock_minimo
        self.__activo = activo
        self.__codigo_barras = codigo_barras

        self.__fecha_creacion = fecha_creacion or datetime.now().isoformat()
        self.__fecha_actualizacion = fecha_actualizacion or datetime.now().isoformat()

    def to_dict(self):
        return {
            "sku": self.__sku,
            "codigo_barras": self.__codigo_barras,
            "nombre_producto": self.__nombre_producto,
            "categoria": self.__categoria,
            "descripcion": self.__descripcion,
            "unidad": self.__unidad,
            "precio_compra": self.__precio_compra,
            "precio_venta": self.__precio_venta,
            "stock_actual": self.__stock_actual,
            "stock_minimo": self.__stock_minimo,
            "activo": self.__activo,
            "fecha_creacion": self.__fecha_creacion,
            "fecha_actualizacion": self.__fecha_actualizacion
        }

    # Properties para que el repository funcione
    @property
    def sku(self): return self.__sku

    @property
    def codigo_barras(self): return self.__codigo_barras

    @property
    def nombre_producto(self): return self.__nombre_producto

    @property
    def categoria(self): return self.__categoria

    @property
    def descripcion(self): return self.__descripcion

    @property
    def unidad(self): return self.__unidad

    @property
    def precio_compra(self): return self.__precio_compra

    @property
    def precio_venta(self): return self.__precio_venta

    @property
    def stock_actual(self): return self.__stock_actual

    @property
    def stock_minimo(self): return self.__stock_minimo

    @property
    def activo(self): return self.__activo

    @property
    def fecha_creacion(self): return self.__fecha_creacion

    @property
    def fecha_actualizacion(self): return self.__fecha_actualizacion

    @fecha_creacion.setter
    def fecha_creacion(self, value):
        self.__fecha_creacion = value

    @fecha_actualizacion.setter
    def fecha_actualizacion(self, value):
        self.__fecha_actualizacion = value

    @activo.setter
    def activo(self, value):
        self.__activo = value