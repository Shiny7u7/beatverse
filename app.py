from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
from models.clientes import ClientesMySQL
from models.pedidos import PedidosMySQL
from models.usuarios import UsuariosMySQL, Usuario
from models.paises import PaisMySQL
from models.ciudades import CiudadMySQL
from models.estados import EstadosMySQL
from models.bitacoras import BitacoraMySQL
from models.permisos import PermisosMySQL
from models.roles import RolesMySQL
from models.tablas import TablaMySQL
import logging

# Configurar el registro de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
app.secret_key = "tu_secreto"

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Especifica la vista de login para redirecciones
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."


@login_manager.user_loader
def load_user(user_id):
    usuario_data = UsuariosMySQL.obtenerUsuarioPorId(user_id)  # Obtener datos del usuario por ID
    if usuario_data:
        return Usuario(usuario_data['usuario_id'], usuario_data['usuario_nombre'], usuario_data['usuario_email'])
    
    return None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        usuario = UsuariosMySQL.obtenerUsuarioPorCorreo(correo)
        
        # Comparación directa de contraseñas en texto plano
        if usuario['usuario_contrasena'] == contrasena:
            user = Usuario(usuario['usuario_id'], usuario['usuario_nombre'], usuario['usuario_email'])
            login_user(user)  # Inicia la sesión del usuario
            print("Usuario autenticado con éxito:", usuario['usuario_nombre'])
            return redirect(url_for('principal'))
        else:
            flash("Contraseña incorrecta.")
            print("Contraseña proporcionada:", contrasena)
            print("Contraseña en la base de datos:", usuario['usuario_contrasena'])
            return redirect(url_for('login'))



    print("Mostrando la página de inicio de sesión.")
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()  # Cierra la sesión del usuario
    return redirect(url_for('login'))  # Redirige a la vista de login


@app.route('/principal')
@login_required
def principal():
    print("El usuario ha accedido a la página principal.")
    return render_template('principal.html')

#-----------------------------------------Usuarios-----------------------------------------#
@app.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    if request.method == 'POST':
        if 'guardar' in request.form:
            usuario_nombre = request.form.get('usuario_nombre')
            usuario_primerapellido = request.form.get('usuario_primerapellido')
            usuario_segundoapellido = request.form.get('usuario_segundoapellido', '')  # Puede ser opcional
            usuario_email = request.form.get('usuario_email')
            usuario_contrasena = request.form.get('usuario_contrasena')
            usuario_rol_id = request.form.get('rol')  # Asegúrate de pasar el ID del rol
            usuario_estado_id = request.form.get('estado')  # Asegúrate de pasar el ID del estado

            # Verificación de datos obligatorios
            if not usuario_nombre or not usuario_email or not usuario_contrasena or not usuario_rol_id or not usuario_estado_id:
                flash("Faltan datos", 'warning')
                logging.warning("No se proporcionaron todos los datos obligatorios para crear un usuario.")
            else:
                # Log simple antes de intentar agregar
                logging.info(f"Intentando agregar usuario: {usuario_nombre}, {usuario_email}")

                # Intentar agregar el usuario
                if UsuariosMySQL.ingresarUsuarios(usuario_nombre, usuario_primerapellido, usuario_segundoapellido, usuario_email, usuario_contrasena, usuario_rol_id, usuario_estado_id):
                    flash("El usuario fue guardado.", "success")
                    logging.info("El usuario fue guardado exitosamente.")
                else:
                    flash("No se pudo guardar el usuario.", "danger")
                    logging.error("Error al intentar guardar el usuario en la base de datos.")

            return redirect(url_for('usuarios'))



        elif 'modificar' in request.form:
            usuario_id = request.form.get('usuario_id')
            usuario_nombre = request.form.get('usuario_nombre')
            usuario_primerapellido = request.form.get('usuario_primerapellido')
            usuario_segundoapellido = request.form.get('usuario_segundoapellido', '')  # Manejar como opcional
            usuario_email = request.form.get('usuario_email')
            usuario_contrasena = request.form.get('usuario_contrasena')
            usuario_rol_id = request.form.get('rol')
            usuario_estado_id = request.form.get('estado')

            if not usuario_id or not usuario_nombre or not usuario_email or not usuario_rol_id or not usuario_estado_id:
                flash("Faltan datos para actualizar el usuario.", 'warning')
            else:
                if UsuariosMySQL.modificarUsuario(usuario_id, usuario_nombre, usuario_primerapellido, usuario_segundoapellido, usuario_email, usuario_contrasena, usuario_rol_id, usuario_estado_id):
                    flash("Los datos del usuario fueron modificados.", "success")
                else:
                    flash("No se pudo modificar el usuario.", "danger")
            return redirect(url_for('usuarios'))


        elif 'eliminar' in request.form:
            usuario_id = request.form['usuario_id']
            if not usuario_id:
                flash("Faltan datos", 'warning')
            else:
                UsuariosMySQL.eliminarUsuario(usuario_id)
                flash("El usuario fue eliminado.", "success")
                return redirect(url_for('usuarios'))

    lista_usuarios = UsuariosMySQL.mostrarUsuario()
    return render_template('usuarios.html', usuarios=lista_usuarios, username=current_user.id, active_page='usuarios', title="Usuarios")


#-----------------------------------------País-----------------------------------------#
@app.route('/pais', methods=['GET', 'POST'])
@login_required
def pais():
    if request.method == 'POST':
        if 'guardar' in request.form:
            descripcion = request.form.get('descripcion')
            if not descripcion:
                flash("Faltan datos", 'warning')
            else:
                # Debugging: imprime el valor de descripcion
                print(f"Descripción recibida: {descripcion}")
                PaisMySQL.ingresarPais(descripcion)
                flash("El país fue guardado.", "success")
                return redirect(url_for('pais'))
        elif 'modificar' in request.form:
            pais_id = request.form['pais_id']
            descripcion = request.form['descripcion']
            if not pais_id or not descripcion:
                flash("Faltan datos", 'warning')
            else:
                PaisMySQL.modificarPais(pais_id, descripcion)
                flash("Los datos fueron modificados.", "success")
                return redirect(url_for('pais'))
        elif 'eliminar' in request.form:
            pais_id = request.form['pais_id']
            if not pais_id:
                flash("Faltan datos", 'warning')
            else:
                PaisMySQL.eliminarPais(pais_id)
                flash("El país fue eliminado.", "success")
                return redirect(url_for('pais'))
    lista_paises = PaisMySQL.mostrarPaises()
    return render_template('paises.html', paises=lista_paises, username=current_user.id, active_page='pais', title="País")

#-----------------------------------------Ciudad-----------------------------------------#
@app.route('/ciudad', methods=['GET', 'POST'])
@login_required
def ciudad():
    if request.method == 'POST':
        if 'guardar' in request.form:
            ciudad_descripcion = request.form['ciudad_descripcion']
            pais_id = request.form['pais_id']  # Asegúrate de tener un campo para el ID del país
            if not ciudad_descripcion or not pais_id:
                flash("Faltan datos", 'warning')
            else:
                if CiudadMySQL.ingresarCiudad(ciudad_descripcion, pais_id):
                    flash("La ciudad fue guardada.", "success")
                else:
                    flash("No se pudo guardar la ciudad.", "danger")
                return redirect(url_for('ciudad'))

        elif 'modificar' in request.form:
            ciudad_id = request.form['ciudad_id']
            ciudad_descripcion = request.form['ciudad_descripcion']
            pais_id = request.form['pais_id']  # Asegúrate de tener el campo para el ID del país
            if not ciudad_id or not ciudad_descripcion or not pais_id:
                flash("Faltan datos", 'warning')
            else:
                if CiudadMySQL.modificarCiudad(ciudad_id, ciudad_descripcion, pais_id):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar la ciudad.", "danger")
                return redirect(url_for('ciudad'))

        elif 'eliminar' in request.form:
            ciudad_id = request.form['ciudad_id']
            if not ciudad_id:
                flash("Faltan datos", 'warning')
            else:
                if CiudadMySQL.eliminarCiudad(ciudad_id):
                    flash("La ciudad fue eliminada.", "success")
                else:
                    flash("No se pudo eliminar la ciudad.", "danger")
                return redirect(url_for('ciudad'))

    lista_ciudades = CiudadMySQL.mostrarCiudad()  # Cambié 'mostrar_ciudades' a 'mostrarCiudad'
    return render_template('ciudades.html', ciudades=lista_ciudades, username=current_user.id, active_page='ciudad', title="Ciudad")


#-----------------------------------------Estado-----------------------------------------#
@app.route('/estado', methods=['GET', 'POST'])
@login_required
def estado():
    if request.method == 'POST':
        if 'guardar' in request.form:
            estado_descripcion = request.form['estado_descripcion']  # Cambié el nombre del campo para que coincida con tu código
            ciudad_id = request.form['ciudad_id']  # Asegúrate de tener un campo para el ID de la ciudad
            if not estado_descripcion or not ciudad_id:
                flash("Faltan datos", 'warning')
            else:
                if EstadosMySQL.ingresarEstado(estado_descripcion, ciudad_id):
                    flash("El estado fue guardado.", "success")
                else:
                    flash("No se pudo guardar el estado.", "danger")
                return redirect(url_for('estado'))

        elif 'modificar' in request.form:
            estado_id = request.form['estado_id']
            estado_descripcion = request.form['estado_descripcion']  # Cambié el nombre del campo para que coincida con tu código
            ciudad_id = request.form['ciudad_id']  # Asegúrate de tener el campo para el ID de la ciudad
            if not estado_id or not estado_descripcion or not ciudad_id:
                flash("Faltan datos", 'warning')
            else:
                if EstadosMySQL.modificarEstado(estado_id, estado_descripcion, ciudad_id):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar el estado.", "danger")
                return redirect(url_for('estado'))

        elif 'eliminar' in request.form:
            estado_id = request.form['estado_id']
            if not estado_id:
                flash("Faltan datos", 'warning')
            else:
                if EstadosMySQL.eliminarEstado(estado_id):
                    flash("El estado fue eliminado.", "success")
                else:
                    flash("No se pudo eliminar el estado.", "danger")
                return redirect(url_for('estado'))

    lista_estados = EstadosMySQL.mostrarEstado()  # Cambié 'mostrar_estados' a 'mostrarEstado'
    return render_template('estados.html', estados=lista_estados, username=current_user.id, active_page='estado', title="Estado")


#-----------------------------------------Clientes-----------------------------------------#
@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    if request.method == 'POST':
        if 'guardar' in request.form:
            cliente_nombre = request.form['cliente_nombre']
            cliente_apellido1 = request.form['cliente_primerapellido']
            cliente_apellido2 = request.form['cliente_segundoapellido']
            cliente_email = request.form['cliente_email']
            cliente_contrasena = request.form['cliente_contrasena']  # Asegúrate de que esto se envíe desde el formulario
            if not cliente_nombre or not cliente_email:
                flash("Faltan datos", 'warning')
            else:
                if ClientesMySQL.ingresarCliente(cliente_nombre, cliente_apellido1, cliente_apellido2, cliente_email, cliente_contrasena):
                    flash("El cliente fue guardado.", "success")
                else:
                    flash("No se pudo guardar el cliente.", "danger")
                return redirect(url_for('clientes'))

        elif 'modificar' in request.form:
            cliente_id = request.form['cliente_id']
            cliente_nombre = request.form['cliente_nombre']
            cliente_apellido1 = request.form['cliente_primerapellido']
            cliente_apellido2 = request.form['cliente_segundoapellido']
            cliente_email = request.form['cliente_email']
            cliente_contrasena = request.form['cliente_contrasena']  # Asegúrate de que esto se envíe desde el formulario
            if not cliente_id or not cliente_nombre or not cliente_email:
                flash("Faltan datos", 'warning')
            else:
                if ClientesMySQL.modificarCliente(cliente_id, cliente_nombre, cliente_apellido1, cliente_apellido2, cliente_email, cliente_contrasena):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar el cliente.", "danger")
                return redirect(url_for('clientes'))

        elif 'eliminar' in request.form:
            cliente_id = request.form['cliente_id']
            if not cliente_id:
                flash("Faltan datos", 'warning')
            else:
                if ClientesMySQL.eliminarCliente(cliente_id):
                    flash("El cliente fue eliminado.", "success")
                else:
                    flash("No se pudo eliminar el cliente.", "danger")
                return redirect(url_for('clientes'))

    lista_clientes = ClientesMySQL.mostrarCliente()  # Asegúrate de que el nombre de la función sea correcto
    return render_template('clientes.html', clientes=lista_clientes, username=current_user.id, active_page='clientes', title="Clientes")


#-----------------------------------------Pedidos-----------------------------------------#
@app.route('/pedidos', methods=['GET', 'POST'])
@login_required
def pedidos():
    if request.method == 'POST':
        if 'guardar' in request.form:
            cliente_id = request.form['cliente_id']
            pedido_total = request.form['pedido_total']
            if not cliente_id or not pedido_total:
                flash("Faltan datos", 'warning')
            else:
                if PedidosMySQL.ingresarPedido(cliente_id, pedido_total):
                    flash("El pedido fue guardado.", "success")
                else:
                    flash("No se pudo guardar el pedido.", "danger")
                return redirect(url_for('pedidos'))

        elif 'modificar' in request.form:
            pedido_id = request.form['pedido_id']
            pedido_total = request.form['pedido_total']
            if not pedido_id or not pedido_total:
                flash("Faltan datos", 'warning')
            else:
                if PedidosMySQL.modificarPedido(pedido_id, pedido_total):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar el pedido.", "danger")
                return redirect(url_for('pedidos'))

        elif 'eliminar' in request.form:
            pedido_id = request.form['pedido_id']
            if not pedido_id:
                flash("Faltan datos", 'warning')
            else:
                if PedidosMySQL.eliminarPedido(pedido_id):
                    flash("El pedido fue eliminado.", "success")
                else:
                    flash("No se pudo eliminar el pedido.", "danger")
                return redirect(url_for('pedidos'))

    lista_pedidos = PedidosMySQL.mostrarPedido()  # Asegúrate de que el nombre de la función sea correcto
    return render_template('pedidos.html', pedidos=lista_pedidos, username=current_user.id, active_page='pedidos', title="Pedidos")

#-----------------------------------------Bitácora-----------------------------------------#
@app.route('/bitacora', methods=['GET', 'POST'])
@login_required
def bitacora():
    if request.method == 'POST':
        if 'guardar' in request.form:
            descripcion = request.form['descripcion']
            tabla_id = request.form['tabla_id']  # Asegúrate de que este campo se incluya en el formulario
            if not descripcion or not tabla_id:
                flash("Faltan datos", 'warning')
            else:
                if BitacoraMySQL.ingresarBitacora(descripcion, tabla_id):
                    flash("La bitácora fue guardada.", "success")
                else:
                    flash("No se pudo guardar la bitácora.", "danger")
                return redirect(url_for('bitacora'))

        elif 'modificar' in request.form:
            bitacora_id = request.form['bitacora_id']
            descripcion = request.form['descripcion']
            tabla_id = request.form['tabla_id']  # Asegúrate de que este campo se incluya en el formulario
            if not bitacora_id or not descripcion or not tabla_id:
                flash("Faltan datos", 'warning')
            else:
                if BitacoraMySQL.modificarBitacora(bitacora_id, descripcion, tabla_id):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar la bitácora.", "danger")
                return redirect(url_for('bitacora'))

        elif 'eliminar' in request.form:
            bitacora_id = request.form['bitacora_id']
            if not bitacora_id:
                flash("Faltan datos", 'warning')
            else:
                if BitacoraMySQL.eliminarBitacora(bitacora_id):
                    flash("La bitácora fue eliminada.", "success")
                else:
                    flash("No se pudo eliminar la bitácora.", "danger")
                return redirect(url_for('bitacora'))

    lista_bitacoras = BitacoraMySQL.mostrarBitacora()  # Asegúrate de que el nombre de la función sea correcto
    return render_template('bitacoras.html', bitacoras=lista_bitacoras, username=current_user.id, active_page='bitacora', title="Bitácora")

#-----------------------------------------Permisos-----------------------------------------#
@app.route('/permisos', methods=['GET', 'POST'])
@login_required
def permisos():
    if request.method == 'POST':
        if 'guardar' in request.form:
            permiso_descripcion = request.form['permiso_descripcion']
            if not permiso_descripcion:
                flash("Faltan datos", 'warning')
            else:
                if PermisosMySQL.ingresarPermiso(permiso_descripcion):
                    flash("El permiso fue guardado.", "success")
                else:
                    flash("No se pudo guardar el permiso.", "danger")
                return redirect(url_for('permisos'))
                
        elif 'modificar' in request.form:
            permiso_id = request.form['permiso_id']
            permiso_descripcion = request.form['permiso_descripcion']
            if not permiso_id or not permiso_descripcion:
                flash("Faltan datos", 'warning')
            else:
                if PermisosMySQL.modificarPermiso(permiso_id, permiso_descripcion):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar el permiso.", "danger")
                return redirect(url_for('permisos'))

        elif 'eliminar' in request.form:
            permiso_id = request.form['permiso_id']
            if not permiso_id:
                flash("Faltan datos", 'warning')
            else:
                if PermisosMySQL.eliminarPermiso(permiso_id):
                    flash("El permiso fue eliminado.", "success")
                else:
                    flash("No se pudo eliminar el permiso.", "danger")
                return redirect(url_for('permisos'))

    lista_permisos = PermisosMySQL.mostrarPermiso()
    return render_template('permisos.html', permisos=lista_permisos, username=current_user.id, active_page='permisos', title="Permisos")


#-----------------------------------------Roles-----------------------------------------#
@app.route('/roles', methods=['GET', 'POST'])
@login_required
def roles():
    if request.method == 'POST':
        if 'guardar' in request.form:
            rol_descripcion = request.form['rol_descripcion']
            if not rol_descripcion:
                flash("Faltan datos", 'warning')
            else:
                if RolesMySQL.ingresarRol(rol_descripcion):
                    flash("El rol fue guardado.", "success")
                else:
                    flash("No se pudo guardar el rol.", "danger")
                return redirect(url_for('roles'))

        elif 'modificar' in request.form:
            rol_id = request.form['rol_id']
            rol_descripcion = request.form['rol_descripcion']
            if not rol_id or not rol_descripcion:
                flash("Faltan datos", 'warning')
            else:
                if RolesMySQL.modificarRol(rol_id, rol_descripcion):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar el rol.", "danger")
                return redirect(url_for('roles'))

        elif 'eliminar' in request.form:
            rol_id = request.form['rol_id']
            if not rol_id:
                flash("Faltan datos", 'warning')
            else:
                if RolesMySQL.eliminarRol(rol_id):
                    flash("El rol fue eliminado.", "success")
                else:
                    flash("No se pudo eliminar el rol.", "danger")
                return redirect(url_for('roles'))

    lista_roles = RolesMySQL.mostrarRol()
    return render_template('roles.html', roles=lista_roles, username=current_user.id, active_page='roles', title="Roles")

#-----------------------------------------Tablas-----------------------------------------#
@app.route('/tablas', methods=['GET', 'POST'])
@login_required
def tablas():
    if request.method == 'POST':
        if 'guardar' in request.form:
            tabla_descripcion = request.form.get('tabla_descripcion')
            if not tabla_descripcion:
                flash("Faltan datos", 'warning')
            else:
                if TablaMySQL.ingresarTabla(tabla_descripcion):
                    flash("La tabla fue guardada.", "success")
                else:
                    flash("No se pudo guardar la tabla.", "danger")
            return redirect(url_for('tablas'))


        elif 'modificar' in request.form:
            tabla_id = request.form['tabla_id']
            tabla_descripcion = request.form['tabla_descripcion']
            if not tabla_id or not tabla_descripcion:
                flash("Faltan datos", 'warning')
            else:
                if TablaMySQL.modificarTabla(tabla_id, tabla_descripcion):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar la tabla.", "danger")
                return redirect(url_for('tablas'))

        elif 'eliminar' in request.form:
            tabla_id = request.form['tabla_id']
            if not tabla_id:
                flash("Faltan datos", 'warning')
            else:
                if TablaMySQL.eliminarTabla(tabla_id):
                    flash("La tabla fue eliminada.", "success")
                else:
                    flash("No se pudo eliminar la tabla.", "danger")
                return redirect(url_for('tablas'))

    lista_tablas = TablaMySQL.mostrarTabla()
    return render_template('tablas.html', tablas=lista_tablas, username=current_user.id, active_page='tablas', title="Tablas")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
