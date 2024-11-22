from datetime import datetime
import re


import sys
import os

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append('C:/Users/Ruth/Desktop/proyecto2/db')
from Conexion import Conexion




from enum import Enum 

class Gasto:
    coleccion = "gastos"

    def __init__(self, monto, descripcion, fecha):
        self.__monto = None
        self.__descripcion = None
        self.__fecha = None
        self.__categoria = False

        # Setters para inicializar con validaciones
        try:
            self.monto = monto
            self.descripcion = descripcion
            self.fecha = fecha
            
        except ValueError as e:
            print(f"Error al asignar atributos: {e}")

    # Getters
    @property
    def monto(self):
        return self.__monto

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def fecha(self):
        return self.__fecha

    @property
    def categoria(self):
        return self.__categoria

    # Setters
    @monto.setter
    def monto(self, nuevo_monto):
        try:
            self.__monto = float(nuevo_monto)  # Aseguramos que el monto sea un número
        except ValueError:
            raise ValueError("El monto debe ser un número válido.")

    @descripcion.setter
    def descripcion(self, nueva_descripcion):
        if not nueva_descripcion:
            raise ValueError("La descripción no puede estar vacía.")
        self.__descripcion = nueva_descripcion

    @fecha.setter
    def fecha(self, nueva_fecha):
        # Validar formato de fecha
        try:
            datetime.strptime(nueva_fecha, "%d/%m/%Y")
            self.__fecha = nueva_fecha
        except ValueError:
            raise ValueError("La fecha debe estar en formato dd/mm/yyyy")

    # Métodos para la base de datos
    def crear_gasto(self):
        coleccion_gasto = Conexion.abrir_conexion()[Gasto.coleccion]
        gasto_existente = coleccion_gasto.find_one({"monto": self.monto})
    
        if gasto_existente:
            print(f"El gasto de '{self.monto}' ya existe.")
            Conexion.cerrar_conexion()
            return
        else:
            datos_gasto = {
                "monto": self.monto,
                "descripcion": self.descripcion,
                "fecha": self.fecha,
                "categoria": self.categoria,
            }
            coleccion_gasto.insert_one(datos_gasto)
            print(f"Gasto '{self.monto}' guardado en la base de datos.")
            Conexion.cerrar_conexion()

    def mostrar_informacion(self):
        estado = "Completada" if self.__categoria else "Pendiente"
        return (f"Gasto: {self.__monto} | Descripción: {self.__descripcion} | "
                f"Fecha límite: {self.__fecha} | Estado: {estado}")

    @classmethod
    def leer_gasto(cls):
        coleccion_gasto = Conexion.abrir_conexion()[cls.coleccion]
        gastos = coleccion_gasto.find()
        for gasto in gastos:
            print(gasto)
        Conexion.cerrar_conexion()

    @classmethod
    def eliminar_gasto(cls, fecha):
        coleccion_gasto = Conexion.abrir_conexion()[cls.coleccion]
        gasto_existente = coleccion_gasto.delete_one({"fecha": fecha})
        Conexion.cerrar_conexion()
        if gasto_existente.deleted_count > 0:
            print(f"Gasto con fecha {fecha} ha sido eliminada.")
        else:
            print(f"Gasto con fecha {fecha} no encontrada.")

    @classmethod
    def actualizar_gasto(cls, fecha, **kwargs):
        coleccion_gasto = Conexion.abrir_conexion()[cls.coleccion]
        gasto_existente = coleccion_gasto.find_one({"fecha": fecha})
        if not gasto_existente:
            return f"El gasto con fecha {fecha} no existe"
        
        gasto_temporal = Gasto(
            monto=gasto_existente["monto"],
            descripcion=gasto_existente["descripcion"],
            fecha=gasto_existente["fecha"],
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
            coleccion_gasto.update_one({"fecha": fecha}, {"$set": cambios})
            print(f"Gasto con fecha {fecha} actualizada.")
        else:
            print("No se realizaron cambios.")
        Conexion.cerrar_conexion()

    def completar_gasto(self):
        self.__categoria = True


if __name__ == "__main__":

    gasto1 = Gasto("200", "compras supermercado", "15/11/2024")
    gasto1.crear_gasto()
    gasto2 = Gasto("150", "alquiler", "17/11/2024")
    
    # Leer todos los gastos
    Gasto.leer_gasto()

    # Eliminar un gasto por fecha
    gasto2.eliminar_gasto("17/11/2024")
    
    # Crear un gasto nuevo
    gasto2.crear_gasto()

    # Actualizar un gasto
    gasto1_actualizada = Gasto.actualizar_gasto("15/11/2024", descripcion="manutención y pensiones")
    print(gasto1_actualizada)
