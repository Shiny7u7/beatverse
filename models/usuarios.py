#models/usuarios.py

from models.db import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql

class UsuariosMySQL:

    @staticmethod
    def obtenerUsuarioPorCorreo(correo):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor(pymysql.cursors.DictCursor)  # Usar DictCursor para obtener resultados como diccionarios
            print(f"Obteniendo usuario con correo: {correo}")  # Para depuración
            sql = """
                SELECT usuario_id, usuario_nombre, usuario_primerapellido, usuario_segundoapellido, usuario_email, usuario_contrasena, rol_id 
                FROM usuario 
                WHERE usuario_email = %s AND usuario_status = 'Ok'
            """
            cursor.execute(sql, (correo,))
            result = cursor.fetchone()
            print(f"Resultado de la consulta: {result}")  # Para depuración

            if result:
                return {
                    'id': result['usuario_id'],
                    'nombre': result['usuario_nombre'],
                    'primerapellido': result['usuario_primerapellido'],
                    'segundoapellido': result['usuario_segundoapellido'],
                    'correo': result['usuario_email'],
                    'contrasena': result['usuario_contrasena'],
                    'rol_id': result['rol_id']
                }
            else:
                print("No se encontró el usuario con ese correo.")
                return None
        except pymysql.Error as error:
            print(f"Error al obtener el usuario por correo: {error}")
            return None
        finally:
            cursor.close()
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
                SELECT u.usuario_id, u.usuario_nombre, u.usuario_primerapellido, u.usuario_segundoapellido, u.usuario_email, u.usuario_contrasena,r.rol_descripcion, u.estado_id, e.estado_descripcion 
                FROM usuario u 
                JOIN rol r ON u.rol_id = r.rol_id
                LEFT JOIN estado e ON u.estado_id = e.estado_id
                WHERE u.usuario_status = 'Ok';
            """
            print(f"Ejecutando consulta: {sql_query}")
            cursor.execute(sql_query)
            resultado = cursor.fetchall()

            print(f"Resultado de la consulta: {resultado}")  # Mensaje para depurar

            return resultado

        except pymysql.MySQLError as e:
            print(f"Error de MySQL al mostrar usuarios: {e}")
            flash("Hubo un error al intentar cargar los usuarios.")
            return []

        except Exception as e:
            print(f"Error inesperado al mostrar usuarios: {e}")
            return []

        finally:
            if cursor is not None:
                cursor.close()
            if cone is not None:
                cone.close()

    @staticmethod
    def ingresarUsuarios(nombre, apellido1, apellido2, correo, contra, rol):
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuario")
            tids = cursor.fetchone()[0] + 1
            fechmodi = datetime.now()
            sql = """
                INSERT INTO usuario 
                (usuario_id, usuario_nombre, usuario_primerapellido, usuario_segundoapellido, usuario_email, usuario_contrasena, rol_id, usuario_status, usuario_fechamodificacion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            values = (tids, nombre, apellido1, apellido2, correo, contra, rol, 'Ok', fechmodi)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Ahora hay {tids} registros en la tabla")
        except pymysql.Error as error:
            print(f"Error de ingreso de datos: {error}")
            flash("Error al guardar el usuario.")
        finally:
            cursor.close()
            cone.close()

    @staticmethod
    def modificarUsuario(id, nombre, apellido1, apellido2, correo, contra, rol):
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
                    usuario_fechamodificacion = %s 
                WHERE usuario_id = %s
            """
            values = (nombre, apellido1, apellido2, correo, contra, rol, fechmodi, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Usuario con ID {id} fue actualizado.")
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")
            flash("Error al modificar el usuario.")
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
            cursor = cone.cursor(pymysql.cursors.DictCursor)  # Usar DictCursor para resultados como diccionarios
            print(f"Obteniendo usuario con ID: {id}")  # Depuración
            sql = "SELECT usuario_id, usuario_nombre, usuario_primerapellido, usuario_segundoapellido, usuario_email, usuario_contrasena, rol_id FROM usuario WHERE usuario_id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            print(f"Resultado de la consulta: {result}")  # Depuración

            if result:
                return {
                    'id': result['usuario_id'],
                    'nombre': result['usuario_nombre'],
                    'primerapellido': result['usuario_primerapellido'],
                    'segundoapellido': result['usuario_segundoapellido'],
                    'correo': result['usuario_email'],
                    'contrasena': result['usuario_contrasena'],
                    'rol_id': result['rol_id']
                }
            else:
                return None
        except pymysql.Error as error:
            print(f"Error al obtener el usuario: {error}")
            return None
        finally:
            cursor.close()
            cone.close()

