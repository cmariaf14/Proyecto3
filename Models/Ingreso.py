class Ingreso(Transaccion):
    def __init__(self, monto, fecha, descripcion, categoria, fuente):
        super().__init__(monto, fecha, descripcion, categoria)
        self.__fuente = fuente

    @property
    def fuente(self):
        return self.__fuente

    @fuente.setter
    def fuente(self, value):
        self.__fuente = value

    def mostrar_informacion(self):
        return f"Ingreso: {self.monto} - Fecha: {self.fecha} - Fuente: {self.fuente} - Descripción: {self.descripcion} - Categoría: {self.categoria.nombre}"

    def actualizar_fuente(self, fuente):
        self.fuente = fuente

    def guardar_en_db(self):
        ingreso = {
            "monto": self.monto,
            "fecha": self.fecha,
            "descripcion": self.descripcion,
            "categoria": self.categoria.nombre,
            "fuente": self.fuente,
            "tipo": "Ingreso"
        }
        coleccion_transacciones.insert_one(ingreso)

    def actualizar_en_db(self):
        coleccion_transacciones.update_one(
            {"descripcion": self.descripcion, "fecha": self.fecha},
            {"$set": {"monto": self.monto, "fuente": self.fuente}}
        )

    def eliminar_de_db(self):
        coleccion_transacciones.delete_one({"descripcion": self.descripcion, "fecha": self.fecha})

    @staticmethod
    def leer_de_db(descripcion):
        documento = coleccion_transacciones.find_one({"descripcion": descripcion})
        if documento and documento["tipo"] == "Ingreso":
            categoria = Categoria(documento["categoria"], "")
            return Ingreso(documento["monto"], documento["fecha"], documento["descripcion"], categoria, documento["fuente"])
        return None
