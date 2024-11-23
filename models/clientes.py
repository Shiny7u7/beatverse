from models.db import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ClientesMySQL:
    @staticmethod
    def mostrarCliente():
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            cliente_id, 
                            cliente_nombre, 
                            cliente_primerapellido, 
                            cliente_segundoapellido, 
                            cliente_email 
                        FROM cliente 
                        WHERE cliente_status = 'Ok';
                    """
                    logging.info(f"Ejecutando consulta: {sql_query}")
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()
                    logging.info(f"Resultado de la consulta: {resultado}")
                    return resultado
        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar clientes: {e}")
            flash("Hubo un error al intentar cargar los clientes.")
            return []
        except Exception as e:
            logging.error(f"Error inesperado al mostrar clientes: {e}")
            flash("Ocurrió un error inesperado al cargar los clientes.")
            return []

    @staticmethod
    def ingresarCliente(cliente, apellido1, apellido2, correo, contra):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    # Alternativa para obtener el siguiente ID de cliente
                    cursor.execute("SELECT COALESCE(MAX(cliente_id), 0) + 1 FROM cliente")
                    tids = cursor.fetchone()[0]  # Usa COALESCE para manejar el caso donde no hay clientes

                    fechmodi = datetime.now()
                    sql = """
                        INSERT INTO cliente 
                        (cliente_id, cliente_nombre, cliente_primerapellido, cliente_segundoapellido, cliente_email, cliente_contrasena, rol_id, cliente_status, cliente_fechamodificacion) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    values = (tids, cliente, apellido1, apellido2, correo, contra, '5', 'Ok', fechmodi)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Cliente agregado: {cliente}.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al guardar cliente: {error}")
            flash("Error al guardar el cliente.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al ingresar cliente: {e}")
            flash("Ocurrió un error inesperado al ingresar el cliente.")
            return False

    @staticmethod
    def modificarCliente(id, nombre, apellido1, apellido2, correo, contra):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = """
                        UPDATE cliente 
                        SET cliente_nombre = %s, 
                            cliente_primerapellido = %s, 
                            cliente_segundoapellido = %s, 
                            cliente_email = %s, 
                            cliente_contrasena = %s, 
                            rol_id = %s, 
                            cliente_fechamodificacion = %s 
                        WHERE cliente_id = %s
                    """
                    values = (nombre, apellido1, apellido2, correo, contra, '5', fechmodi, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    logging.info(f"Cliente con ID {id} fue actualizado.")
                    return True
        except pymysql.Error as error:
            logging.error(f"Error al modificar los datos: {error}")
            flash("Error al modificar el cliente.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al modificar cliente: {e}")
            flash("Ocurrió un error inesperado al modificar el cliente.")
            return False

    @staticmethod
    def eliminarCliente(id):
        try:
            with ConexionMySQL.conexion() as cone:
                with cone.cursor() as cursor:
                    fechmodi = datetime.now()
                    sql = "UPDATE cliente SET cliente_status = 'No', cliente_fechamodificacion = %s WHERE cliente_id = %s"
                    values = (fechmodi, id)
                    cursor.execute(sql, values)
                    cone.commit()
                    if cursor.rowcount > 0:
                        logging.info(f"Cliente con ID {id} fue eliminado.")
                        return True
                    else:
                        logging.warning(f"No se encontró el cliente con ID {id} para eliminar.")
                        return False
        except pymysql.Error as error:
            logging.error(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar el cliente.")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al eliminar cliente: {e}")
            flash("Ocurrió un error inesperado al eliminar el cliente.")
            return False
