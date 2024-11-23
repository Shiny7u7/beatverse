import pymysql
from config import Config

class ConexionMySQL:
    @staticmethod
    def conexion():
        """Establece la conexión a la base de datos MySQL."""
        try:
            conexion = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                db=Config.MYSQL_DB,
                port=Config.MYSQL_PORT,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            return conexion
        except pymysql.MySQLError as error:
            print(f"Error al conectarse a la Base de Datos: {error}")
            return None
