from models.conexion import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CiudadMySQL:
    @staticmethod
    def mostrarCiudad():
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            c.ciudad_id, 
                            c.ciudad_descripcion, 
                            c.pais_id,
                            p.pais_descripcion
                        FROM ciudad c
                        LEFT JOIN pais p ON c.pais_id = p.pais_id
                        WHERE ciudad_status = 'Ok';
                    """
                    logging.info(f"Ejecutando consulta: {sql_query}")
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()
                    logging.info(f"Resultado de la consulta: {resultado}")
                    return resultado
        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar ciudades: {e}")
            flash("Hubo un error al intentar cargar las ciudades.")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al mostrar ciudades: {e}")
            flash("Ocurrió un error inesperado al cargar las ciudades.")
            return []

    @staticmethod
    def ingresarCiudad(ciudad_descripcion, pais_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    # Alternativa para obtener el siguiente ID de ciudad
                    cursor.execute("SELECT COALESCE(MAX(ciudad_id), 0) + 1 FROM ciudad")
                    nueva_ciudad_id = cursor.fetchone()[0]  # Usa COALESCE para manejar el caso donde no hay ciudades

                    fechmodi = datetime.now()
                    sql = """
                        INSERT INTO ciudad 
                        (ciudad_id, ciudad_descripcion, pais_id, ciudad_status, ciudad_fechamodificacion) 
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    values = (nueva_ciudad_id, ciudad_descripcion, pais_id, 'Ok', fechmodi)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Ciudad agregada: {ciudad_descripcion}.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al guardar ciudad: {error}")
            flash("Error al guardar la ciudad.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al ingresar ciudad: {e}")
            flash("Ocurrió un error inesperado al ingresar la ciudad.")
            return False

    @staticmethod
    def modificarCiudad(ciudad_id, ciudad_descripcion, pais_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = """
                        UPDATE ciudad 
                        SET ciudad_descripcion = %s, 
                            pais_id = %s, 
                            ciudad_fechamodificacion = %s 
                        WHERE ciudad_id = %s
                    """
                    values = (ciudad_descripcion, pais_id, fechmodi, ciudad_id)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Ciudad con ID {ciudad_id} fue actualizada.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al modificar los datos: {error}")
            flash("Error al modificar la ciudad.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al modificar ciudad: {e}")
            flash("Ocurrió un error inesperado al modificar la ciudad.")
            return False

    @staticmethod
    def eliminarCiudad(ciudad_id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = "UPDATE ciudad SET ciudad_status = 'No', ciudad_fechamodificacion = %s WHERE ciudad_id = %s"
                    values = (fechmodi, ciudad_id)
                    cursor.execute(sql, values)
                    cone.commit()
                    if cursor.rowcount > 0:
                        logging.info(f"Ciudad con ID {ciudad_id} fue eliminada.")
                        return True
                    else:
                        logging.warning(f"No se encontró la ciudad con ID {ciudad_id} para eliminar.")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar la ciudad.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al eliminar ciudad: {e}")
            flash("Ocurrió un error inesperado al eliminar la ciudad.")
            return False
