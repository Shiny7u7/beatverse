from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.ciudades import CiudadMySQL  # Asegúrate de que el nombre del archivo y la clase sean correctos

api_ciudades = Blueprint('ciudades', __name__, url_prefix='/ciudades')

@api_ciudades.route('/', methods=['GET'])
def ciudades():
    try:
        # Cargar la lista de ciudades desde la base de datos
        ciudades = CiudadMySQL.mostrarCiudad()
        return render_template('ciudades.html', ciudades=ciudades)
    except Exception as e:
        print(f"Error al cargar la página de ciudades: {e}")
        flash("Ocurrió un error al cargar las ciudades.")
        return render_template('ciudades.html', ciudades=[])


@api_ciudades.route('/api/ciudades', methods=['GET', 'POST'])
def obtener_ciudades():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Agrega esto para depurar
        ciudad_descripcion = data.get('ciudad_descripcion')
        pais_id = data.get('pais_id')

        if ciudad_descripcion and pais_id:
            CiudadMySQL.ingresarCiudad(ciudad_descripcion, pais_id)
            return {"message": "Ciudad ingresada correctamente"}, 201
        return {"message": "Todos los campos son requeridos"}, 400

    # Método GET para retornar todas las ciudades
    ciudades = CiudadMySQL.mostrarCiudad()
    return jsonify(ciudades), 200


@api_ciudades.route('/api/ciudades/<int:id>', methods=['PUT'])
def modificar_ciudad(id):
    data = request.get_json()
    ciudad_descripcion = data.get('ciudad_descripcion')
    pais_id = data.get('pais_id')

    # Verificar que todos los campos requeridos están presentes
    if not all([ciudad_descripcion, pais_id]):
        return {"message": "Todos los campos son requeridos"}, 400

    try:
        # Intentar modificar la ciudad
        success = CiudadMySQL.modificarCiudad(id, ciudad_descripcion, pais_id)
        if success:  # Asegúrate de que este método retorna True/False o maneja excepciones adecuadamente
            return {"message": "Ciudad modificada correctamente"}, 200
        else:
            return {"message": "Error al modificar la ciudad"}, 500
    except Exception as e:
        print(f"Error inesperado al modificar ciudad: {e}")  # Para depurar el error
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_ciudades.route('/api/ciudades/<int:id>', methods=['DELETE'])
def eliminar_ciudad(id):
    try:
        success = CiudadMySQL.eliminarCiudad(id)
        if success:
            return {"message": "Ciudad eliminada correctamente"}, 204
        else:
            return {"message": "Error al eliminar la ciudad"}, 500
    except Exception as e:
        print(f"Error inesperado al eliminar ciudad: {e}")
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_ciudades.route('/api/ciudades/<int:id>', methods=['GET'])
def obtener_ciudad_por_id(id):
    ciudad = CiudadMySQL.obtenerCiudadPorId(id)  # Asegúrate de tener este método definido en CiudadMySQL
    if ciudad:
        return jsonify(ciudad), 200
    else:
        return {"message": "Ciudad no encontrada"}, 404
