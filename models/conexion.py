import pymysql

class ConexionMySQL:
    @staticmethod
    def conexion():
        """Establece la conexión a la base de datos MySQL."""
        try:
            conexion = pymysql.connect(
                host="34.134.65.19",
                user="taco",
                password="12345",
                db="musica",
                port=3306,  # Asegúrate de que el puerto es correcto
                charset="utf8mb4",  # Especifica el conjunto de caracteres, si es necesario
                cursorclass=pymysql.cursors.DictCursor  # Usa un cursor dict para retornar filas como diccionarios, si se desea
            )
            print("Conexión correcta")
            return conexion
        except pymysql.MySQLError as error:
            print(f"Error al conectarse a la Base de Datos: {error}")
            return None