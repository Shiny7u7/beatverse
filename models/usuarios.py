from models.conexion import ConexionMySQL
from flask_login import UserMixin
from datetime import datetime
from pymysql.cursors import DictCursor
from flask import flash
import pymysql
import logging

# Configurar el registro de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Usuario(UserMixin):
    def __init__(self, id, nombre, correo):
        self.id = id          # ID único del usuario
        self.nombre = nombre  # Nombre del usuario
        self.correo = correo

class UsuariosMySQL:


    @staticmethod
    def obtenerUsuarioPorCorreo(correo):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor(DictCursor)  # Usar DictCursor para acceder por nombres de columna
            sql = """
                SELECT usuario_id, usuario_nombre, usuario_email, usuario_contrasena 
                FROM usuario 
                WHERE usuario_email = %s AND usuario_status = 'Ok'
            """
            cursor.execute(sql, (correo,))
            result = cursor.fetchone()  # Obtiene una fila del resultado

            if result:
                return result  # Devuelve el resultado si se encontró el usuario
            else:
                print("Usuario no encontrado o inactivo.")
                return None
                
        except pymysql.Error as error:
            print(f"Error al obtener el usuario: {error}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if cone is not None:
                cone.close()

    @staticmethod
    def obtenerUsuarioPorId(user_id):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor(DictCursor)
            sql = """
                SELECT usuario_id, usuario_nombre, usuario_email, usuario_contrasena 
                FROM usuario 
                WHERE usuario_id = %s
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()  # Obtiene una fila del resultado

            if result:
                return result  # Devuelve el resultado si se encontró el usuario
            else:
                return None
                
        except pymysql.Error as error:
            print(f"Error al obtener el usuario: {error}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if cone is not None:
                cone.close()


    @staticmethod
    def mostrarUsuario():
        cone = None
        cursor = None
        try:
            cone = ConexionMySQL.conexion()
            if cone is None:
                raise Exception("No se pudo conectar a la base de datos.")
            cursor = cone.cursor()

            sql_query = """
                SELECT u.usuario_id, u.usuario_nombre, u.usuario_primerapellido, u.usuario_segundoapellido, 
                    u.usuario_email, u.usuario_contrasena, u.rol_id, r.rol_descripcion, 
                    u.estado_id, e.estado_descripcion 
                FROM usuario u 
                JOIN rol r ON u.rol_id = r.rol_id
                LEFT JOIN estado e ON u.estado_id = e.estado_id
                WHERE u.usuario_status = 'Ok';
            """
            logging.info(f"Ejecutando consulta: {sql_query}")
            cursor.execute(sql_query)
            resultado = cursor.fetchall()

            logging.info(f"Resultado de la consulta: {resultado}")  # Mensaje para depurar

            return resultado

        except pymysql.MySQLError as e:
            logging.error(f"Error de MySQL al mostrar usuarios: {e}")
            flash("Hubo un error al intentar cargar los usuarios.")
            return []

        except Exception as e:
            logging.error(f"Error inesperado al mostrar usuarios: {e}")
            return []

        finally:
            if cursor is not None:
                cursor.close()
            if cone is not None:
                cone.close()


    @staticmethod
    def ingresarUsuarios(nombre, apellido1, apellido2, correo, contra, rol, estado):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()

            # Generar el siguiente usuario_id de forma segura
            cursor.execute("SELECT COALESCE(MAX(usuario_id), 0) + 1 FROM usuario")
            usuario_id = cursor.fetchone()[0]

            fechmodi = datetime.now()
            sql = """
                INSERT INTO usuario 
                (usuario_id, usuario_nombre, usuario_primerapellido, usuario_segundoapellido, usuario_email, usuario_contrasena, rol_id, estado_id, usuario_status, usuario_fechamodificacion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (usuario_id, nombre, apellido1, apellido2, correo, contra, rol, estado, 'Ok', fechmodi)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Usuario agregado correctamente con ID {usuario_id}")
            return True
        except pymysql.Error as error:
            print(f"Error al guardar el usuario: {error}")
            flash("Error al guardar el usuario.")
            return False
        finally:
            cursor.close()
            cone.close()



    @staticmethod
    def modificarUsuario(id, nombre, apellido1, apellido2, correo, contra, rol, estado):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            fechmodi = datetime.now()
            sql = """
                UPDATE usuario 
                SET usuario_nombre = %s, 
                    usuario_primerapellido = %s, 
                    usuario_segundoapellido = %s, 
                    usuario_email = %s, 
                    usuario_contrasena = %s, 
                    rol_id = %s, 
                    estado_id = %s,
                    usuario_fechamodificacion = %s 
                WHERE usuario_id = %s
            """
            values = (nombre, apellido1, apellido2, correo, contra, rol, estado, fechmodi, id)
            print(f"Actualizando usuario con ID {id} con los valores: {values}")  # Log para depurar
            cursor.execute(sql, values)
            cone.commit()
            if cursor.rowcount > 0:
                print(f"Usuario con ID {id} fue actualizado.")
                return True
            else:
                print(f"No se encontró el usuario con ID {id}.")
                return False
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")
            flash("Error al modificar el usuario.")
            return False
        finally:
            cursor.close()
            cone.close()




    @staticmethod
    def eliminarUsuario(id):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            fechmodi = datetime.now()
            sql = "UPDATE usuario SET usuario_status = 'No', usuario_fechamodificacion = %s WHERE usuario_id = %s"
            values = (fechmodi, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Usuario con ID {id} fue eliminada.")
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar el usuario.")
        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def obtenerUsuario(id):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            print(f"Obteniendo usuario con ID: {id}")  # Depuración
            sql = "SELECT usuario_id, usuario_nombre, usuario_primerapellido, usuario_segundoapellido, usuario_email, usuario_contrasena, rol_id FROM usuario WHERE usuario_id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            print(f"Resultado de la consulta: {result}")  # Depuración

            if result:
                return {
                    'id': result[0],
                    'nombre': result[1],
                    'primerapellido': result[2],
                    'segundoapellido': result[3],
                    'correo': result[4],
                    'contrasena': result[5],
                    'rol_id': result[6]
                }
            else:
                return None
        except pymysql.Error as error:
            print(f"Error al obtener el usuario: {error}")
            return None
        finally:
            cursor.close()
            cone.close()

    

        
        
