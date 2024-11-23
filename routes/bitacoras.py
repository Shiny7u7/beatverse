from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.bitacoras import BitacoraMySQL

api_bitacora = Blueprint('bitacora', __name__, url_prefix='/bitacora')

@api_bitacora.route('/', methods=['GET'])
def bitacora():
    try:
        # Cargar la lista de bitácoras desde la base de datos
        bitacoras = BitacoraMySQL.mostrarBitacora()
        return render_template('bitacora.html', bitacoras=bitacoras)
    except Exception as e:
        print(f"Error al cargar la página de bitácora: {e}")
        flash("Ocurrió un error al cargar la bitácora.")
        return render_template('bitacora.html', bitacoras=[])


@api_bitacora.route('/api/bitacora', methods=['GET', 'POST'])
def obtener_bitacora():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Agrega esto para depurar
        bitacora_descripcion = data.get('bitacora_descripcion')
        tabla_id = data.get('tabla_id')

        if bitacora_descripcion and tabla_id:
            BitacoraMySQL.ingresarBitacora(bitacora_descripcion, tabla_id)
            return {"message": "Bitácora ingresada correctamente"}, 201
        return {"message": "Todos los campos son requeridos"}, 400

    # Método GET para retornar todas las bitácoras
    bitacoras = BitacoraMySQL.mostrarBitacora()
    return jsonify(bitacoras), 200


@api_bitacora.route('/api/bitacora/<int:id>', methods=['PUT'])
def modificar_bitacora(id):
    data = request.get_json()
    bitacora_descripcion = data.get('bitacora_descripcion')
    tabla_id = data.get('tabla_id')

    # Verificar que todos los campos requeridos están presentes
    if not all([bitacora_descripcion, tabla_id]):
        return {"message": "Todos los campos son requeridos"}, 400

    try:
        # Intentar modificar la bitácora
        success = BitacoraMySQL.modificarBitacora(id, bitacora_descripcion, tabla_id)
        if success:  # Asegúrate de que este método retorna True/False o maneja excepciones adecuadamente
            return {"message": "Bitácora modificada correctamente"}, 200
        else:
            return {"message": "Error al modificar la bitácora"}, 500
    except Exception as e:
        print(f"Error inesperado al modificar bitácora: {e}")  # Para depurar el error
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_bitacora.route('/api/bitacora/<int:id>', methods=['DELETE'])
def eliminar_bitacora(id):
    try:
        success = BitacoraMySQL.eliminarBitacora(id)
        if success:
            return {"message": "Bitácora eliminada correctamente"}, 204
        else:
            return {"message": "Error al eliminar la bitácora"}, 500
    except Exception as e:
        print(f"Error inesperado al eliminar bitácora: {e}")
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_bitacora.route('/api/bitacora/<int:id>', methods=['GET'])
def obtener_bitacora_por_id(id):
    bitacora = BitacoraMySQL.obtenerBitacoraPorId(id)  # Asegúrate de tener este método en BitacoraMySQL
    if bitacora:
        return jsonify(bitacora), 200
    else:
        return {"message": "Bitácora no encontrada"}, 404
