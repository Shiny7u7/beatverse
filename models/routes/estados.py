from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.estados import EstadosMySQL  # Asegúrate de que el nombre del archivo y la clase coincidan

api_estados = Blueprint('estados', __name__, url_prefix='/estados')

@api_estados.route('/', methods=['GET'])
def estados():
    try:
        # Cargar la lista de estados desde la base de datos
        estados = EstadosMySQL.mostrarEstado()
        return render_template('estados.html', estados=estados)
    except Exception as e:
        print(f"Error al cargar la página de estados: {e}")
        flash("Ocurrió un error al cargar los estados.")
        return render_template('estados.html', estados=[])


@api_estados.route('/api/estados', methods=['GET', 'POST'])
def obtener_estados():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Agrega esto para depurar
        descripcion = data.get('descripcion')
        ciudad_id = data.get('ciudad_id')
        
        if descripcion and ciudad_id:
            EstadosMySQL.ingresarEstado(descripcion, ciudad_id)
            return {"message": "Estado ingresado correctamente"}, 201
        return {"message": "Todos los campos son requeridos"}, 400

    # Método GET para retornar todos los estados
    estados = EstadosMySQL.mostrarEstado()
    return jsonify(estados), 200


@api_estados.route('/api/estados/<int:id>', methods=['PUT'])
def modificar_estado(id):
    data = request.get_json()
    descripcion = data.get('descripcion')
    ciudad_id = data.get('ciudad_id')

    # Verificar que todos los campos requeridos están presentes
    if not all([descripcion, ciudad_id]):
        return {"message": "Todos los campos son requeridos"}, 400

    try:
        # Intentar modificar el estado
        success = EstadosMySQL.modificarEstado(id, descripcion, ciudad_id)
        if success:  # Asegúrate de que este método retorna True/False o maneja excepciones adecuadamente
            return {"message": "Estado modificado correctamente"}, 200
        else:
            return {"message": "Error al modificar el estado"}, 500
    except Exception as e:
        print(f"Error inesperado al modificar estado: {e}")  # Para depurar el error
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_estados.route('/api/estados/<int:id>', methods=['DELETE'])
def eliminar_estado(id):
    try:
        success = EstadosMySQL.eliminarEstado(id)
        if success:
            return {"message": "Estado eliminado correctamente"}, 204
        else:
            return {"message": "Error al eliminar el estado"}, 500
    except Exception as e:
        print(f"Error inesperado al eliminar estado: {e}")
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_estados.route('/api/estados/<int:id>', methods=['GET'])
def obtener_estado_por_id(id):
    estado = EstadosMySQL.obtenerEstadoPorId(id)  # Asegúrate de tener este método en tu clase EstadosMySQL
    if estado:
        return jsonify(estado), 200
    else:
        return {"message": "Estado no encontrado"}, 404
