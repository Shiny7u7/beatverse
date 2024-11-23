from models.db import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql

class RolesMySQL:
    @staticmethod
    def mostrarRol():
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            cursor.execute("SELECT * FROM rol WHERE rol_status = 'Ok'")
            miResultado = cursor.fetchall()
            return miResultado
        except pymysql.Error as error:
            flash(f"Error al cargar roles: {error}")
            return []
        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def ingresarRol(rol):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            fechmodi = datetime.now()
            sql = """
                INSERT INTO rol 
                (rol_descripcion, rol_status, rol_fechamodificacion) 
                VALUES (%s, %s, %s);
            """
            values = (rol, 'Ok', fechmodi)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Rol '{rol}' ingresado correctamente.")
        except pymysql.Error as error:
            flash(f"Error al guardar el rol: {error}")
        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarRol(id, rol):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            fechmodi = datetime.now()
            sql = "UPDATE rol SET rol_descripcion = %s, rol_fechamodificacion = %s WHERE rol_id = %s"
            values = (rol, fechmodi, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Rol con ID {id} fue actualizado a '{rol}'.")
        except pymysql.Error as error:
            flash(f"Error al modificar el rol: {error}")
        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def eliminarRol(id):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            fechmodi = datetime.now()
            sql = "UPDATE rol SET rol_status = 'No', rol_fechamodificacion = %s WHERE rol_id = %s"
            values = (fechmodi, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Rol con ID {id} fue eliminado.")
        except pymysql.Error as error:
            flash(f"Error al eliminar el rol: {error}")
        finally:
            cursor.close()
            cone.close()
