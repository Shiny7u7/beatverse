from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.roles import RolesMySQL
import pymysql

api_roles = Blueprint('roles', __name__, url_prefix='/roles')

# Ruta para la página de Roles
@api_roles.route('/', methods=['GET', 'POST'])
def roles():
    if request.method == 'POST':
        rol = request.form.get('rol')
        if rol:
            RolesMySQL.ingresarRol(rol)
            flash("Rol ingresado correctamente.")
        else:
            flash("El nombre del rol es requerido.")
    roles = RolesMySQL.mostrarRol()
    return render_template('roles.html', roles=roles)

# API para obtener todos los roles
@api_roles.route('/api/roles', methods=['GET'])
def obtener_roles():
    roles = RolesMySQL.mostrarRol()
    return jsonify(roles)

# API para obtener un rol específico
@api_roles.route('/api/roles/<int:id>', methods=['GET'])
def api_obtener_rol(id):
    rol = RolesMySQL.obtenerRol(id)  # Asegúrate de que tienes este método en tu modelo
    if rol:
        return jsonify({
            'rol_id': rol['id'],
            'rol_descripcion': rol['descripcion'],
        }), 200
    else:
        return jsonify({"error": "Rol no encontrado."}), 404

# Ruta para modificar un rol
@api_roles.route('/modificar_rol/<int:id>', methods=['POST'])
def modificar_rol(id):
    rol = request.form.get('rol')
    if rol:
        RolesMySQL.modificarRol(id, rol)
        flash("Rol modificado correctamente.")
    else:
        flash("El nombre del rol es requerido.")
    return redirect(url_for('roles.roles'))

# API para modificar un rol
@api_roles.route('/api/roles/<int:id>', methods=['PUT'])
def api_modificar_rol(id):
    data = request.json
    rol = data.get('rol')
    if rol:
        RolesMySQL.modificarRol(id, rol)
        return jsonify({"message": "Rol modificado correctamente."}), 200
    else:
        return jsonify({"error": "El nombre del rol es requerido."}), 400

# Ruta para eliminar un rol
@api_roles.route('/eliminar_rol/<int:id>')
def eliminar_rol(id):
    RolesMySQL.eliminarRol(id)
    flash("Rol eliminado correctamente.")
    return redirect(url_for('roles.roles'))

# API para eliminar un rol
@api_roles.route('/api/roles/<int:id>', methods=['DELETE'])
def api_eliminar_rol(id):
    RolesMySQL.eliminarRol(id)
    return jsonify({"message": "Rol eliminado correctamente."}), 200
