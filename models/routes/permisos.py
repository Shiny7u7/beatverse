from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.permisos import PermisosMySQL

api_permisos = Blueprint('permisos', __name__, url_prefix='/permisos')

@api_permisos.route('/', methods=['GET'])
def permisos():
    try:
        # Cargar la lista de permisos desde la base de datos
        permisos = PermisosMySQL.mostrarPermiso()
        return render_template('permisos.html', permisos=permisos)
    except Exception as e:
        print(f"Error al cargar la página de permisos: {e}")
        flash("Ocurrió un error al cargar los permisos.")
        return render_template('permisos.html', permisos=[])


@api_permisos.route('/api/permisos', methods=['GET', 'POST'])
def obtener_permisos():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Agrega esto para depurar
        descripcion = data.get('descripcion')
        
        if descripcion:
            PermisosMySQL.ingresarPermiso(descripcion)
            return {"message": "Permiso ingresado correctamente"}, 201
        return {"message": "El campo descripción es requerido"}, 400

    # Método GET para retornar todos los permisos
    permisos = PermisosMySQL.mostrarPermiso()
    return jsonify(permisos), 200


@api_permisos.route('/api/permisos/<int:id>', methods=['PUT'])
def modificar_permiso(id):
    data = request.get_json()
    descripcion = data.get('descripcion')

    # Verificar que el campo requerido está presente
    if not descripcion:
        return {"message": "El campo descripción es requerido"}, 400

    try:
        # Intentar modificar el permiso
        success = PermisosMySQL.modificarPermiso(id, descripcion)
        if success:  # Asegúrate de que este método retorna True/False o maneja excepciones adecuadamente
            return {"message": "Permiso modificado correctamente"}, 200
        else:
            return {"message": "Error al modificar el permiso"}, 500
    except Exception as e:
        print(f"Error inesperado al modificar permiso: {e}")  # Para depurar el error
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_permisos.route('/api/permisos/<int:id>', methods=['DELETE'])
def eliminar_permiso(id):
    try:
        success = PermisosMySQL.eliminarPermiso(id)
        if success:
            return {"message": "Permiso eliminado correctamente"}, 204
        else:
            return {"message": "Error al eliminar el permiso"}, 500
    except Exception as e:
        print(f"Error inesperado al eliminar permiso: {e}")
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_permisos.route('/api/permisos/<int:id>', methods=['GET'])
def obtener_permiso_por_id(id):
    permiso = PermisosMySQL.obtenerPermisoPorId(id)
    if permiso:
        return jsonify(permiso), 200
    else:
        return {"message": "Permiso no encontrado"}, 404
