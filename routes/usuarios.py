from flask import Blueprint, request, jsonify, session
from flask_cors import CORS
from models.usuarios import UsuariosMySQL

# Crear el Blueprint para usuarios
api_usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Habilitar CORS para este Blueprint
CORS(api_usuarios, supports_credentials=True)

# Ruta para inicio de sesión
@api_usuarios.route('/inicio_sesion', methods=['POST'])
def login():
    try:
        # Obtener datos JSON del frontend
        data = request.get_json()

        # Extraer correo y contraseña
        correo = data.get('correo')
        contrasena = data.get('contrasena')

        # Validar que los campos no estén vacíos
        if not correo or not contrasena:
            return jsonify({
                "success": False,
                "message": "Por favor ingrese el correo y la contraseña."
            }), 400

        # Consultar el usuario en la base de datos
        usuario = UsuariosMySQL.obtenerUsuarioPorCorreo(correo)

        # Verificar si el usuario existe y si la contraseña coincide
        if usuario and usuario['contrasena'] == contrasena:
            # Guardar datos en la sesión (opcional)
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            session['usuario_rol'] = usuario['rol_id']

            # Respuesta exitosa con datos del usuario
            return jsonify({
                "success": True,
                "usuario": {
                    "id": usuario['id'],
                    "nombre": usuario['nombre'],
                    "correo": usuario['correo'],
                    "rol_id": usuario['rol_id']
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Correo o contraseña incorrectos."
            }), 401
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error en el servidor.",
            "error": str(e)
        }), 500


# Ruta para cerrar sesión
@api_usuarios.route('/cerrar_sesion', methods=['POST'])
def logout():
    try:
        # Limpiar la sesión
        session.clear()
        return jsonify({"success": True, "message": "Sesión cerrada correctamente."}), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al cerrar sesión.",
            "error": str(e)
        }), 500

# Ruta para obtener todos los usuarios (API)
@api_usuarios.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        usuarios = UsuariosMySQL.mostrarUsuario()
        usuarios_con_detalles = []
        
        # Añadir correo y contrasena a los usuarios obtenidos
        for usuario in usuarios:
            usuarios_con_detalles.append({
                'usuario_id': usuario['usuario_id'],
                'usuario_nombre': usuario['usuario_nombre'],
                'usuario_primerapellido': usuario['usuario_primerapellido'],
                'usuario_segundoapellido': usuario['usuario_segundoapellido'],
                'correo': usuario['usuario_email'],
                'contrasena': usuario['usuario_contrasena'],
                'rol_descripcion': usuario['rol_descripcion']
            })
        return jsonify(usuarios_con_detalles), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener usuarios.", "details": str(e)}), 500

# Ruta para obtener un usuario específico (API)
@api_usuarios.route('/api/usuarios/<int:id>', methods=['GET'])
def api_obtener_usuario(id):
    try:
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
    except Exception as e:
        return jsonify({"error": "Error al obtener el usuario.", "details": str(e)}), 500

# Ruta para modificar un usuario (API)
@api_usuarios.route('/api/usuarios/<int:id>', methods=['PUT'])
def api_modificar_usuario(id):
    try:
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
    except Exception as e:
        return jsonify({"error": "Error al modificar el usuario.", "details": str(e)}), 500

# Ruta para eliminar un usuario (API)
@api_usuarios.route('/api/usuarios/<int:id>', methods=['DELETE'])
def api_eliminar_usuario(id):
    try:
        UsuariosMySQL.eliminarUsuario(id)
        return jsonify({"message": "Usuario eliminado correctamente."}), 200
    except Exception as e:
        return jsonify({"error": "Error al eliminar el usuario.", "details": str(e)}), 500
