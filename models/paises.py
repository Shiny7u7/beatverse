from models.conexion import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PaisMySQL:
    @staticmethod
    def mostrarPaises():
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            pais_id, 
                            pais_descripcion 
                        FROM pais 
                        WHERE pais_status = 'Ok';
                    """
                    logging.info(f"Ejecutando consulta: {sql_query}")
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()
                    logging.info(f"Resultado de la consulta: {resultado}")
                    return resultado
        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar países: {e}")
            flash("Hubo un error al intentar cargar los países.")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al mostrar países: {e}")
            flash("Ocurrió un error inesperado al cargar los países.")
            return []

    @staticmethod
    def ingresarPais(descripcion):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    # Alternativa para obtener el siguiente ID de país
                    cursor.execute("SELECT COALESCE(MAX(pais_id), 0) + 1 FROM pais")
                    pais_id = cursor.fetchone()[0]  # Usa COALESCE para manejar el caso donde no hay países

                    fechamodificacion = datetime.now()
                    sql = """
                        INSERT INTO pais 
                        (pais_id, pais_descripcion, pais_status, pais_fechamodificacion) 
                        VALUES (%s, %s, %s, %s);
                    """
                    values = (pais_id, descripcion, 'Ok', fechamodificacion)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"País agregado: {descripcion}.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al guardar el país: {error}")
            flash("Error al guardar el país.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al ingresar país: {e}")
            flash("Ocurrió un error inesperado al ingresar el país.")
            return False




    @staticmethod
    def modificarPais(id, descripcion):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechamodificacion = datetime.now()
                    sql = """
                        UPDATE pais 
                        SET pais_descripcion = %s, 
                            pais_fechamodificacion = %s 
                        WHERE pais_id = %s
                    """
                    values = (descripcion, fechamodificacion, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"País con ID {id} fue actualizado.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al modificar los datos: {error}")
            flash("Error al modificar el país.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al modificar país: {e}")
            flash("Ocurrió un error inesperado al modificar el país.")
            return False

    @staticmethod
    def eliminarPais(id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechamodificacion = datetime.now()
                    sql = "UPDATE pais SET pais_status = 'No', pais_fechamodificacion = %s WHERE pais_id = %s"
                    values = (fechamodificacion, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    if cursor.rowcount > 0:
                        logging.info(f"País con ID {id} fue eliminado.")
                        return True
                    else:
                        logging.warning(f"No se encontró el país con ID {id} para eliminar.")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar el país.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al eliminar país: {e}")
            flash("Ocurrió un error inesperado al eliminar el país.")
            return False
