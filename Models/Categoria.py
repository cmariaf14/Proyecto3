from datetime import datetime
import re
from db import Conexion
from enum import Enum 


class Categoria:
    coleccion = "gastos"

    def __init__(self, nombre, descripcion, transaccion, ):
        self.__nombre = None
        self.__descripcion = None
        self.__transaccion = None
  
        # Setters para inicializar con validaciones
        try:
            self.nombre = nombre
            self.descripcion = descripcion
            self.transaccion = transaccion
            
        except ValueError as e:
            print(f"Error al asignar atributos: {e}")

    # Getters
    @property
    def nombre(self):
        return self.__nombre

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def transaccion(self):
        return self.__transaccion


    # Setters
    @nombre.setter
    def nombre(self, nuevo_titulo):
        self.__nombre = nuevo_titulo

    @descripcion.setter
    def descripcion(self, nueva_descripcion):
        self.__descripcion = nueva_descripcion

    @transaccion.setter
    def transaccion(self, nueva_fecha):
        # Validar formato de transaccion
        try:
            datetime.strptime(nueva_fecha, "%d/%m/%Y")
            self.__transaccion = nueva_fecha
        except ValueError:
            raise ValueError("La transaccion debe estar en formato dd/mm/yyyy")


    # Métodos para la base de datos
    def crear_gasto(self):
        coleccion_gasto = Conexion.abrir_conexion()[Categoria.coleccion]
        gasto_existente = coleccion_gasto.find_one({"nombre": self.nombre})
    
        if gasto_existente:
            print(f"La gasto '{self.nombre}' ya existe")
            Conexion.cerrar_conexion()
            return
        else:
            datos_gasto = {
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "transaccion": self.transaccion,
                "categoria": self.categoria,
            }
            coleccion_gasto.insert_one(datos_gasto)
            print(f"Categoria '{self.nombre}' guardada en la base de datos")
            Conexion.cerrar_conexion()

    def mostrar_informacion(self):
        estado = "Completada" if self.__categoria else "Pendiente"
        return (f"Categoria: {self.__nombre} | Descripción: {self.__descripcion} | "
                f"Fecha límite: {self.__transaccion} |  Estado: {estado}")

    @classmethod
    def leer_gasto(cls):
        coleccion_gasto = Conexion.abrir_conexion()[cls.coleccion]
        gastos = coleccion_gasto.find()
        for gasto in gastos:
            print(gasto)
        Conexion.cerrar_conexion()

    @classmethod
    def eliminar_gasto(cls, transaccion):
        coleccion_gasto = Conexion.abrir_conexion()[cls.coleccion]
        gasto_existente = coleccion_gasto.delete_one({"transaccion": transaccion})
        Conexion.cerrar_conexion()
        if gasto_existente.deleted_count > 0:
            print(f"Categoria con transaccion {transaccion} ha sido eliminada.")
        else:
            print(f"Categoria con transaccion {transaccion} no encontrada.")

    @classmethod
    def actualizar_gasto(cls, transaccion, **kwargs):
        coleccion_gasto = Conexion.abrir_conexion()[cls.coleccion]
        gasto_existente = coleccion_gasto.find_one({"transaccion": transaccion})
        if not gasto_existente:
            return f"La gasto con transaccion {transaccion} no existe"
        
        gasto_temporal = Categoria(
            nombre=gasto_existente["nombre"],
            descripcion=gasto_existente["descripcion"],
            transaccion=gasto_existente["transaccion"],
          
        )

        cambios = {}
        for atributo, nuevo_valor in kwargs.items():
            try:
                setattr(gasto_temporal, atributo, nuevo_valor)
                if getattr(gasto_temporal, atributo) != gasto_existente[atributo]:
                    cambios[atributo] = getattr(gasto_temporal, atributo)
            except ValueError as e:
                return f"Error al actualizar {atributo}: {e}"

        if cambios:
            coleccion_gasto.update_one({"transaccion": transaccion}, {"$set": cambios})
            print(f"Categoria con transaccion {transaccion} actualizada.")
        else:
            print("No se realizaron cambios.")
        Conexion.cerrar_conexion()

    def completar_gasto(self):
        self.__categoria = True

if __name__ == "__main__":

    gasto1 = Categoria("200", "compras supermercado", "15/11/2024")
    gasto1.crear_gasto()
    gasto2 = Categoria("150", "alquiler", "17/11/2024")
    
    #cliente2 = Cliente("34523643", "Ana Lopez", "ana@example.com", "Calle antigua 321")
    #cliente3 = Cliente("12234456", "Ruth Puelles Lopez", "ruth@example.com", "Calle antigua 1234545")

    # Crear un cliente y guardarlo en la base de datos
    #gasto1.crear_gasto()

    Categoria.leer_gasto()

    #eliminar el cliente
    #gasto2.eliminar_gasto("17/11/2024")
    #gasto2.crear_gasto()
    #actualizar cliente
    #gasto1_actualizada = Categoria.actualizar_gasto("15/11/2024", descripcion= "manutension y pensiones")
    #print(gasto1_actualizada)