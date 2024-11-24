from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.usuarios import UsuariosMySQL
from models.roles import RolesMySQL

api_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Ruta de inicio de sesión
@api_usuarios.route('/inicio_sesion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        if not correo or not contrasena:
            flash("Por favor ingrese el correo y la contraseña.", "warning")
            return render_template('inicio_sesion.html')

        usuario = UsuariosMySQL.obtenerUsuarioPorCorreo(correo)

        if usuario and usuario['contrasena'] == contrasena:
            flash(f"Bienvenido {usuario['nombre']}!", "success")
            return redirect(url_for('usuarios.principal'))
        else:
            flash("Correo o contraseña incorrectos.", "danger")
    
    return render_template('inicio_sesion.html')

# Ruta para la página principal
@api_usuarios.route('/principal')
def principal():
    return render_template('principal.html')

# Ruta para cerrar sesión
@api_usuarios.route('/cerrar_sesion')
def logout():
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('usuarios.login'))

# Página de usuarios
@api_usuarios.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        idi = request.form.get('id')
        nombre = request.form.get('nombre')
        apellido1 = request.form.get('apellido1')
        apellido2 = request.form.get('apellido2')
        correo = request.form.get('correo')
        contra = request.form.get('contra')
        rol = request.form.get('rol')

        if nombre and apellido1 and correo and contra:
            try:
                UsuariosMySQL.ingresarUsuarios(idi, nombre, apellido1, apellido2, correo, contra, rol)
                flash("Usuario ingresado correctamente.")
            except Exception as e:
                flash(f"Error al ingresar el usuario: {e}")
        else:
            flash("Todos los campos son requeridos.")
    
    usuarios = UsuariosMySQL.mostrarUsuario()
    return render_template('usuarios.html', usuarios=usuarios)

# Rutas de la API
@api_usuarios.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = UsuariosMySQL.mostrarUsuario()
    return jsonify(usuarios)

@api_usuarios.route('/api/usuarios/<int:id>', methods=['GET'])
def api_obtener_usuario(id):
    usuario = UsuariosMySQL.obtenerUsuario(id)
    if usuario:
        return jsonify({
            'usuario_id': usuario['id'],
            'usuario_nombre': usuario['nombre'],
            'primerapellido': usuario['primerapellido'],
            'segundoapellido': usuario['segundoapellido'],
            'correo': usuario['correo'],
            'contrasena': usuario['contrasena'],
            'rol_id': usuario['rol_id']
        }), 200
    else:
        return jsonify({"error": "Usuario no encontrado."}), 404

@api_usuarios.route('/api/usuarios', methods=['POST'])
def api_crear_usuario():
    data = request.json
    nombre = data.get('nombre')
    apellido1 = data.get('apellido1')
    apellido2 = data.get('apellido2')
    correo = data.get('correo')
    contra = data.get('contra')
    rol = data.get('rol')

    if nombre and apellido1 and correo and contra:
        try:
            UsuariosMySQL.ingresarUsuarios(None, nombre, apellido1, apellido2, correo, contra, rol)
            return jsonify({"message": "Usuario creado exitosamente."}), 201
        except Exception as e:
            return jsonify({"error": f"Error al crear el usuario: {e}"}), 500
    else:
        return jsonify({"error": "Todos los campos son requeridos."}), 400

@api_usuarios.route('/api/usuarios/<int:id>', methods=['PUT'])
def api_modificar_usuario(id):
    data = request.json
    nombre = data.get('nombre')
    apellido1 = data.get('apellido1')
    apellido2 = data.get('apellido2')
    correo = data.get('correo')
    contra = data.get('contra')
    rol = data.get('rol')

    if nombre and apellido1 and correo and contra:
        UsuariosMySQL.modificarUsuario(id, nombre, apellido1, apellido2, correo, contra, rol)
        return jsonify({"message": "Usuario modificado correctamente."}), 200
    else:
        return jsonify({"error": "Todos los campos son requeridos."}), 400

@api_usuarios.route('/api/usuarios/<int:id>', methods=['DELETE'])
def api_eliminar_usuario(id):
    UsuariosMySQL.eliminarUsuario(id)
    return jsonify({"message": "Usuario eliminado correctamente."}), 200
