from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.tablas import TablaMySQL

api_tablas = Blueprint('tabla', __name__,url_prefix='/tabla')

@api_tablas.route('/', methods=['GET'])
def tabla():
    try:
        # Cargar la lista de tablas desde la base de datos
        tablas = TablaMySQL.mostrarTabla()
        return render_template('tabla.html', tablas=tablas)
    except Exception as e:
        print(f"Error al cargar la página de tablas: {e}")
        flash("Ocurrió un error al cargar las tablas.")
        return render_template('tabla.html', tablas=[])


@api_tablas.route('/api/tablas', methods=['GET', 'POST'])
def obtener_tablas():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Agrega esto para depurar
        descripcion = data.get('descripcion')
        
        if descripcion:
            TablaMySQL.ingresarTabla(descripcion)
            return {"message": "Tabla ingresada correctamente"}, 201
        return {"message": "El campo descripción es requerido"}, 400

    # Método GET para retornar todas las tablas
    tablas = TablaMySQL.mostrarTabla()
    return jsonify(tablas), 200


@api_tablas.route('/api/tablas/<int:id>', methods=['PUT'])
def modificar_tabla(id):
    data = request.get_json()
    descripcion = data.get('descripcion')

    # Verificar que el campo descripción está presente
    if not descripcion:
        return {"message": "El campo descripción es requerido"}, 400

    try:
        # Intentar modificar la tabla
        success = TablaMySQL.modificarTabla(id, descripcion)
        if success:
            return {"message": "Tabla modificada correctamente"}, 200
        else:
            return {"message": "Error al modificar la tabla"}, 500
    except Exception as e:
        print(f"Error inesperado al modificar tabla: {e}")  # Para depurar el error
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_tablas.route('/api/tablas/<int:id>', methods=['DELETE'])
def eliminar_tabla(id):
    try:
        success = TablaMySQL.eliminarTabla(id)
        if success:
            return {"message": "Tabla eliminada correctamente"}, 204
        else:
            return {"message": "Error al eliminar la tabla"}, 500
    except Exception as e:
        print(f"Error inesperado al eliminar tabla: {e}")
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_tablas.route('/api/tablas/<int:id>', methods=['GET'])
def obtener_tabla_por_id(id):
    tabla = TablaMySQL.obtenerTablaPorId(id)
    if tabla:
        return jsonify(tabla), 200
    else:
        return {"message": "Tabla no encontrada"}, 404
