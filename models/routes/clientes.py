from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.clientes import ClientesMySQL

api_clientes = Blueprint('clientes', __name__,url_prefix='/clientes')

@api_clientes.route('/', methods=['GET'])
def clientes():
    try:
        # Cargar la lista de clientes desde la base de datos
        clientes = ClientesMySQL.mostrarCliente()
        return render_template('clientes.html', clientes=clientes)
    except Exception as e:
        print(f"Error al cargar la página de clientes: {e}")
        flash("Ocurrió un error al cargar los clientes.")
        return render_template('clientes.html', clientes=[])


@api_clientes.route('/api/clientes', methods=['GET', 'POST'])
def obtener_clientes():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Datos recibidos: {data}")  # Agrega esto para depurar
        nombre = data.get('nombre')
        apellido1 = data.get('apellido1')
        apellido2 = data.get('apellido2')
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        
        if nombre and apellido1 and correo and contrasena:
            ClientesMySQL.ingresarCliente(nombre, apellido1, apellido2, correo, contrasena)
            return {"message": "Cliente ingresado correctamente"}, 201
        return {"message": "Todos los campos son requeridos"}, 400

    # Método GET para retornar todos los clientes
    clientes = ClientesMySQL.mostrarCliente()
    return jsonify(clientes), 200


@api_clientes.route('/api/clientes/<int:id>', methods=['PUT'])
def modificar_cliente(id):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido1 = data.get('apellido1')
    apellido2 = data.get('apellido2')
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    # Verificar que todos los campos requeridos están presentes
    if not all([nombre, apellido1, correo, contrasena]):
        return {"message": "Todos los campos son requeridos"}, 400

    try:
        # Intentar modificar el cliente
        success = ClientesMySQL.modificarCliente(id, nombre, apellido1, apellido2, correo, contrasena)
        if success:  # Asegúrate de que este método retorna True/False o maneja excepciones adecuadamente
            return {"message": "Cliente modificado correctamente"}, 200
        else:
            return {"message": "Error al modificar el cliente"}, 500
    except Exception as e:
        print(f"Error inesperado al modificar cliente: {e}")  # Para depurar el error
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500



@api_clientes.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    try:
        success = ClientesMySQL.eliminarCliente(id)
        if success:
            return {"message": "Cliente eliminado correctamente"}, 204
        else:
            return {"message": "Error al eliminar el cliente"}, 500
    except Exception as e:
        print(f"Error inesperado al eliminar cliente: {e}")
        return {"message": "Error inesperado. Intente de nuevo más tarde."}, 500


@api_clientes.route('/api/clientes/<int:id>', methods=['GET'])
def obtener_cliente_por_id(id):
    cliente = ClientesMySQL.obtenerClientePorId(id)
    if cliente:
        return jsonify(cliente), 200
    else:
        return {"message": "Cliente no encontrado"}, 404
