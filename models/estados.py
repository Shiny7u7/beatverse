from models.db import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EstadosMySQL:
    @staticmethod
    def mostrarEstado():
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            e.estado_id, 
                            e.estado_descripcion, 
                            c.ciudad_descripcion
                        FROM estado e
                        LEFT JOIN ciudad c ON e.ciudad_id = c.ciudad_id
                        WHERE estado_status = 'Ok';
                    """
                    logging.info(f"Ejecutando consulta: {sql_query}")
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()
                    logging.info(f"Resultado de la consulta: {resultado}")
                    return resultado
        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar estados: {e}")
            flash("Hubo un error al intentar cargar los estados.")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al mostrar estados: {e}")
            flash("Ocurrió un error inesperado al cargar los estados.")
            return []

    @staticmethod
    def ingresarEstado(descripcion, ciudad_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    # Alternativa para obtener el siguiente ID de estado
                    cursor.execute("SELECT COALESCE(MAX(estado_id), 0) + 1 FROM estado")
                    tids = cursor.fetchone()[0]  # Usa COALESCE para manejar el caso donde no hay estados

                    fechmodi = datetime.now()
                    sql = """
                        INSERT INTO estado 
                        (estado_id, estado_descripcion, ciudad_id, estado_status, estado_fechamodificacion) 
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    values = (tids, descripcion, ciudad_id, 'Ok', fechmodi)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Estado agregado: {descripcion}.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al guardar estado: {error}")
            flash("Error al guardar el estado.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al ingresar estado: {e}")
            flash("Ocurrió un error inesperado al ingresar el estado.")
            return False

    @staticmethod
    def modificarEstado(id, descripcion, ciudad_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = """
                        UPDATE estado 
                        SET estado_descripcion = %s, 
                            ciudad_id = %s, 
                            estado_fechamodificacion = %s 
                        WHERE estado_id = %s
                    """
                    values = (descripcion, ciudad_id, fechmodi, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Estado con ID {id} fue actualizado.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al modificar los datos: {error}")
            flash("Error al modificar el estado.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al modificar estado: {e}")
            flash("Ocurrió un error inesperado al modificar el estado.")
            return False

    @staticmethod
    def eliminarEstado(id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = "UPDATE estado SET estado_status = 'No', estado_fechamodificacion = %s WHERE estado_id = %s"
                    values = (fechmodi, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    if cursor.rowcount > 0:
                        logging.info(f"Estado con ID {id} fue eliminado.")
                        return True
                    else:
                        logging.warning(f"No se encontró el estado con ID {id} para eliminar.")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar el estado.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al eliminar estado: {e}")
            flash("Ocurrió un error inesperado al eliminar el estado.")
            return False
