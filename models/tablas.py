from models.conexion import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TablaMySQL:
    @staticmethod
    def mostrarTabla():
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            tabla_id, 
                            tabla_descripcion
                        FROM tabla 
                        WHERE tabla_status = 'Ok';
                    """
                    logging.info(f"Ejecutando consulta: {sql_query}")
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()
                    logging.info(f"Resultado de la consulta: {resultado}")
                    return resultado
        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar las tablas: {e}")
            flash("Hubo un error al intentar cargar las tablas.")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al mostrar las tablas: {e}")
            flash("Ocurrió un error inesperado al cargar las tablas.")
            return []

    @staticmethod
    def ingresarTabla(tabla_descripcion):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    # Obtener el siguiente ID de tabla
                    cursor.execute("SELECT COALESCE(MAX(tabla_id), 0) + 1 FROM tabla")
                    tids = cursor.fetchone()[0]
                    logging.info(f"Siguiente ID para la tabla: {tids}")  # Agregado para depuración

                    fechmodi = datetime.now()
                    sql = """
                        INSERT INTO tabla 
                        (tabla_id, tabla_descripcion, tabla_status, tabla_fechamodificacion) 
                        VALUES (%s, %s, %s, %s);
                    """
                    values = (tids, tabla_descripcion, 'Ok', fechmodi)
                    logging.info(f"Intentando insertar con valores: {values}")
                    cursor.execute(sql, values)
                    cone.commit()

                    # Comprobar si se insertó alguna fila
                    if cursor.rowcount > 0:
                        logging.info(f"Tabla agregada correctamente: {tabla_descripcion} con ID {tids}.")
                        return True
                    else:
                        logging.warning(f"No se insertó la tabla: {tabla_descripcion}")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al guardar tabla: {error}")
            flash("Error al guardar la tabla.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al ingresar tabla: {e}")
            flash("Ocurrió un error inesperado al ingresar la tabla.")
            return False




    @staticmethod
    def modificarTabla(id, descripcion):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = """
                        UPDATE tabla 
                        SET tabla_descripcion = %s, 
                            tabla_fechamodificacion = %s 
                        WHERE tabla_id = %s
                    """
                    values = (descripcion, fechmodi, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Tabla con ID {id} fue actualizada.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al modificar los datos: {error}")
            flash("Error al modificar la tabla.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al modificar tabla: {e}")
            flash("Ocurrió un error inesperado al modificar la tabla.")
            return False

    @staticmethod
    def eliminarTabla(id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = "UPDATE tabla SET tabla_status = 'No', tabla_fechamodificacion = %s WHERE tabla_id = %s"
                    values = (fechmodi, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    if cursor.rowcount > 0:
                        logging.info(f"Tabla con ID {id} fue eliminada.")
                        return True
                    else:
                        logging.warning(f"No se encontró la tabla con ID {id} para eliminar.")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar la tabla.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al eliminar tabla: {e}")
            flash("Ocurrió un error inesperado al eliminar la tabla.")
            return False
