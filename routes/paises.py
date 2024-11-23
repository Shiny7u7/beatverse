from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.paises import PaisMySQL

api_paises = Blueprint('pais', __name__, url_prefix='/pais')

@api_paises.route('/', methods=['GET'])
def paises():
    try:
        # Cargar la lista de países desde la base de datos
        paises = PaisMySQL.mostrarPaises()
        return render_template('paises.html', paises=paises)
    except Exception as e:
        print(f"Error al cargar la página de países: {e}")
        flash("Ocurrió un error al cargar los países.")
        return render_template('paises.html', paises=[])


@api_paises.route('/api/paises', methods=['GET', 'POST'])
def obtener_paises():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Agrega esto para depurar
        descripcion = data.get('descripcion')
        
        if descripcion:
            PaisMySQL.ingresarPais(descripcion)
            return {"message": "País ingresado correctamente"}, 201
        return {"message": "El campo descripción es requerido"}, 400

    # Método GET para retornar todos los países
    paises = PaisMySQL.mostrarPaises()
    return jsonify(paises), 200


@api_paises.route('/api/paises/<int:id>', methods=['PUT'])
def modificar_pais(id):
    data = request.get_json()
    descripcion = data.get('descripcion')

    # Verificar que todos los campos requeridos están presentes
    if not descripcion:
        return {"message": "El campo descripción es requerido"}, 400

    try:
        # Intentar modificar el país
        success = PaisMySQL.modificarPais(id, descripcion)
        if success:  # Asegúrate de que este método retorna True/False o maneja excepciones adecuadamente
            return {"message": "País modificado correctamente"}, 200
        else:
            return {"message": "Error al modificar el país"}, 500
    except Exception as e:
        print(f"Error inesperado al modificar país: {e}")  # Para depurar el error
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_paises.route('/api/paises/<int:id>', methods=['DELETE'])
def eliminar_pais(id):
    try:
        success = PaisMySQL.eliminarPais(id)
        if success:
            return {"message": "País eliminado correctamente"}, 204
        else:
            return {"message": "Error al eliminar el país"}, 500
    except Exception as e:
        print(f"Error inesperado al eliminar país: {e}")
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_paises.route('/api/paises/<int:id>', methods=['GET'])
def obtener_pais_por_id(id):
    pais = PaisMySQL.obtenerPaisPorId(id)
    if pais:
        return jsonify(pais), 200
    else:
        return {"message": "País no encontrado"}, 404
