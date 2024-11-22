#from db import Conexion
from abc import ABC, abstractmethod
from pymongo import MongoClient
class Transaccion(ABC):
    def __init__(self, monto, fecha, descripcion, categoria):
        self.__monto = monto
        self.__fecha = fecha
        self.__descripcion = descripcion
        self.__categoria = categoria

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, value):
        self.__monto = value

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, value):
        self.__fecha = value

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, value):
        self.__descripcion = value

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, value):
        self.__categoria = value

    @abstractmethod
    def mostrar_informacion(self):
        pass

    def crear(self):
        try:
            transaccion = {
                "monto": self.monto,
                "fecha": self.fecha,
                "descripcion": self.descripcion,
                "categoria": self.categoria.nombre,
                "tipo": self.__class__.__name__
            }
            coleccion_transacciones.insert_one(transaccion)
            print("Transacción creada exitosamente.")
        except Exception as e:
            print(f"Error al crear la transacción: {e}")
        finally:
            print("Operación de creación finalizada.")

    @classmethod
    def leer(cls, descripcion):
        try:
            documento = coleccion_transacciones.find_one({"descripcion": descripcion})
            if documento:
                print("Transacción encontrada.")
                return documento
            else:
                print("Transacción no encontrada.")
                return None
        except Exception as e:
            print(f"Error al leer la transacción: {e}")
        finally:
            print("Operación de lectura finalizada.")

    def actualizar(self, nuevos_datos):
        try:
            coleccion_transacciones.update_one(
                {"descripcion": self.descripcion, "fecha": self.fecha},
                {"$set": nuevos_datos}
            )
            print("Transacción actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar la transacción: {e}")
        finally:
            print("Operación de actualización finalizada.")

    def eliminar(self):
        try:
            coleccion_transacciones.delete_one({"descripcion": self.descripcion, "fecha": self.fecha})
            print("Transacción eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la transacción: {e}")
        finally:
            print("Operación de eliminación finalizada.")

