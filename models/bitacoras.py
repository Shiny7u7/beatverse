from models.db import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BitacoraMySQL:
    @staticmethod
    def mostrarBitacora():
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            bitacora_id, 
                            bitacora_descripcion, 
                            tabla_id, 
                            bitacora_status, 
                            bitacora_fechamodificacion 
                        FROM bitacora 
                        WHERE bitacora_status = 'Ok';
                    """
                    logging.info(f"Ejecutando consulta: {sql_query}")
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()
                    logging.info(f"Resultado de la consulta: {resultado}")
                    return resultado
        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar bitácora: {e}")
            flash("Hubo un error al intentar cargar la bitácora.")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al mostrar bitácora: {e}")
            flash("Ocurrió un error inesperado al cargar la bitácora.")
            return []

    @staticmethod
    def ingresarBitacora(bitacora_descripcion, tabla_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    # Alternativa para obtener el siguiente ID de bitácora
                    cursor.execute("SELECT COALESCE(MAX(bitacora_id), 0) + 1 FROM bitacora")
                    nueva_bitacora_id = cursor.fetchone()[0]  # Usa COALESCE para manejar el caso donde no hay bitácoras

                    fechmodi = datetime.now()
                    sql = """
                        INSERT INTO bitacora 
                        (bitacora_id, bitacora_descripcion, tabla_id, bitacora_status, bitacora_fechamodificacion) 
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    values = (nueva_bitacora_id, bitacora_descripcion, tabla_id, 'Ok', fechmodi)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Bitácora agregada: {bitacora_descripcion}.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al guardar bitácora: {error}")
            flash("Error al guardar la bitácora.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al ingresar bitácora: {e}")
            flash("Ocurrió un error inesperado al ingresar la bitácora.")
            return False

    @staticmethod
    def modificarBitacora(bitacora_id, bitacora_descripcion, tabla_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = """
                        UPDATE bitacora 
                        SET bitacora_descripcion = %s, 
                            tabla_id = %s, 
                            bitacora_fechamodificacion = %s 
                        WHERE bitacora_id = %s
                    """
                    values = (bitacora_descripcion, tabla_id, fechmodi, bitacora_id)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Bitácora con ID {bitacora_id} fue actualizada.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al modificar los datos: {error}")
            flash("Error al modificar la bitácora.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al modificar bitácora: {e}")
            flash("Ocurrió un error inesperado al modificar la bitácora.")
            return False

    @staticmethod
    def eliminarBitacora(bitacora_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = "UPDATE bitacora SET bitacora_status = 'No', bitacora_fechamodificacion = %s WHERE bitacora_id = %s"
                    values = (fechmodi, bitacora_id)
                    cursor.execute(sql, values)
                    cone.commit()
                    if cursor.rowcount > 0:
                        logging.info(f"Bitácora con ID {bitacora_id} fue eliminada.")
                        return True
                    else:
                        logging.warning(f"No se encontró la bitácora con ID {bitacora_id} para eliminar.")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar la bitácora.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al eliminar bitácora: {e}")
            flash("Ocurrió un error inesperado al eliminar la bitácora.")
            return False
