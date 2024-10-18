from models.conexion import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PermisosMySQL:
    @staticmethod
    def mostrarPermiso():
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            permiso_id, 
                            permiso_descripcion 
                        FROM permiso 
                        WHERE permiso_status = 'Ok';
                    """
                    logging.info(f"Ejecutando consulta: {sql_query}")
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()
                    logging.info(f"Resultado de la consulta: {resultado}")
                    return resultado
        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar permisos: {e}")
            flash("Hubo un error al intentar cargar los permisos.")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al mostrar permisos: {e}")
            flash("Ocurrió un error inesperado al cargar los permisos.")
            return []

    @staticmethod
    def ingresarPermiso(descripcion):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    # Alternativa para obtener el siguiente ID de permiso
                    cursor.execute("SELECT COALESCE(MAX(permiso_id), 0) + 1 FROM permiso")
                    permiso_id = cursor.fetchone()[0]  # Usa COALESCE para manejar el caso donde no hay permisos

                    fechamodificacion = datetime.now()
                    sql = """
                        INSERT INTO permiso 
                        (permiso_id, permiso_descripcion, permiso_status, permiso_fechamodificacion) 
                        VALUES (%s, %s, %s, %s);
                    """
                    values = (permiso_id, descripcion, 'Ok', fechamodificacion)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Permiso agregado: {descripcion}.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al guardar permiso: {error}")
            flash("Error al guardar el permiso.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al ingresar permiso: {e}")
            flash("Ocurrió un error inesperado al ingresar el permiso.")
            return False

    @staticmethod
    def modificarPermiso(id, descripcion):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechamodificacion = datetime.now()
                    sql = """
                        UPDATE permiso 
                        SET permiso_descripcion = %s, 
                            permiso_fechamodificacion = %s 
                        WHERE permiso_id = %s
                    """
                    values = (descripcion, fechamodificacion, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Permiso con ID {id} fue actualizado.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al modificar los datos: {error}")
            flash("Error al modificar el permiso.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al modificar permiso: {e}")
            flash("Ocurrió un error inesperado al modificar el permiso.")
            return False

    @staticmethod
    def eliminarPermiso(id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechamodificacion = datetime.now()
                    sql = "UPDATE permiso SET permiso_status = 'No', permiso_fechamodificacion = %s WHERE permiso_id = %s"
                    values = (fechamodificacion, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    if cursor.rowcount > 0:
                        logging.info(f"Permiso con ID {id} fue eliminado.")
                        return True
                    else:
                        logging.warning(f"No se encontró el permiso con ID {id} para eliminar.")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar el permiso.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al eliminar permiso: {e}")
            flash("Ocurrió un error inesperado al eliminar el permiso.")
            return False
