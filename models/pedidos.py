from models.conexion import ConexionMySQL
from datetime import datetime
from flask import flash
import pymysql


class PedidosMySQL:
    @staticmethod
    def mostrarPedido():
        # Implementación de mostrar pedidos
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            cursor.execute("SELECT p.pedido_id, p.cliente_id,c.cliente_nombre, p.pedido_fecha, p.pedido_total, p.pedido_status FROM pedido p JOIN cliente c ON p.cliente_id = c.cliente_id WHERE p.pedido_status = 'Ok'")
            miResultado = cursor.fetchall()
            return miResultado
        except pymysql.Error as error:
            print(f"Error al mostrar datos: {error}")
            flash("Error al cargar pedidos.")
            return []
        finally:
            cursor.close()
            cone.close()


    @staticmethod
    def ingresarPedido(cliente_id, total):
        # Implementación de ingresar pedido
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            cursor.execute("SELECT COUNT(*) FROM pedido")
            tids = cursor.fetchone()[0] + 1
            
            # Obtener la fecha actual
            fecha_actual = datetime.now()
            fechmodi = datetime.now()
            sql = """
                INSERT INTO pedido 
                (pedido_id, cliente_id, pedido_fecha, pedido_total, pedido_status, pedido_fechamodificacion, usuario_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            values = (tids, cliente_id, fecha_actual, total, 'Ok', fechmodi, 1)  # usuario_id será siempre 1
            cursor.execute(sql, values)
            cone.commit()
            print(f"Pedido agregado con ID {tids}.")
        except pymysql.Error as error:
            print(f"Error al guardar pedido: {error}")
            flash("Error al guardar el pedido.")
        finally:
            cursor.close()
            cone.close()


    @staticmethod
    def modificarPedido(id, total):
        # Implementación de modificar pedido
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            fechmodi = datetime.now()
            sql = """
                UPDATE pedido 
                SET pedido_total = %s, 
                    pedido_fechamodificacion = %s 
                WHERE pedido_id = %s
            """
            values = (total, fechmodi, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Pedido con ID {id} fue actualizado.")
        except pymysql.Error as error:
            print(f"Error al modificar los datos: {error}")
            flash("Error al modificar el pedido.")
        finally:
            cursor.close()
            cone.close()


    @staticmethod
    def eliminarPedido(id):
        # Implementación de eliminar pedido
        try:
            cone = ConexionMySQL.conexion()
            cursor = cone.cursor()
            fechmodi = datetime.now()
            sql = "UPDATE pedido SET pedido_status = 'No', pedido_fechamodificacion = %s WHERE pedido_id = %s"
            values = (fechmodi, id)
            cursor.execute(sql, values)
            cone.commit()
            print(f"Pedido con ID {id} fue eliminado.")
        except pymysql.Error as error:
            print(f"Error al eliminar los datos: {error}")
            flash("Error al eliminar el pedido.")
        finally:
            cursor.close()
            cone.close()

