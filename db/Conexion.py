from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError

class Conexion:
    _gasto = None
    _bd = None

    @classmethod
    def abrir_conexion(cls, nombre_bd="transaccion_db"):
        try:
            if cls._gasto is None:
                # Cambia la URI según tu configuración
                uri = "mongodb://localhost:27017"
                cls._gasto = MongoClient(uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)
                # Verificar la conexión
                cls._gasto.admin.command('ping')
                print("Conexión exitosa a MongoDB")
            
            cls._bd = cls._gasto[nombre_bd]
            print(f"Base de datos '{nombre_bd}' seleccionada con éxito.")
            return cls._bd
        except ServerSelectionTimeoutError:
            print("No se pudo conectar al servidor de MongoDB. Verifica que esté en ejecución.")
            return None
        except ConfigurationError as e:
            print(f"Error de configuración: {e}")
            return None
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return None

    @classmethod
    def cerrar_conexion(cls):
        if cls._gasto:
            cls._gasto.close()
            print("Conexión cerrada")
            cls._gasto = None
            cls._bd = None


if __name__ == "__main__":
    # Prueba de la conexión
    db = Conexion.abrir_conexion()
    if db is not None:  # Corrección aquí
        print("Conexión y selección de base de datos completadas.")
    else:
        print("No se pudo completar la conexión.")
    Conexion.cerrar_conexion()
