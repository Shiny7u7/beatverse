from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.pedidos import PedidosMySQL

api_pedidos = Blueprint('pedidos', __name__)

# Ruta principal para la página de Pedidos
@api_pedidos.route('/', methods=['GET', 'POST'])
def pedidos():
    if request.method == 'POST':
        # Guardar un nuevo pedido
        if 'guardar' in request.form:
            cliente_id = request.form.get('cliente_id')
            pedido_total = request.form.get('pedido_total')
            if not cliente_id or not pedido_total:
                flash("Faltan datos", 'warning')
            else:
                if PedidosMySQL.ingresarPedido(cliente_id, pedido_total):
                    flash("El pedido fue guardado.", "success")
                else:
                    flash("No se pudo guardar el pedido.", "danger")
            return redirect(url_for('pedidos.pedidos'))

        # Modificar un pedido existente
        elif 'modificar' in request.form:
            pedido_id = request.form.get('pedido_id')
            pedido_total = request.form.get('pedido_total')
            if not pedido_id or not pedido_total:
                flash("Faltan datos", 'warning')
            else:
                if PedidosMySQL.modificarPedido(pedido_id, pedido_total):
                    flash("Los datos fueron modificados.", "success")
                else:
                    flash("No se pudo modificar el pedido.", "danger")
            return redirect(url_for('pedidos.pedidos'))

        # Eliminar un pedido
        elif 'eliminar' in request.form:
            pedido_id = request.form.get('pedido_id')
            if not pedido_id:
                flash("Faltan datos", 'warning')
            else:
                if PedidosMySQL.eliminarPedido(pedido_id):
                    flash("El pedido fue eliminado.", "success")
                else:
                    flash("No se pudo eliminar el pedido.", "danger")
            return redirect(url_for('pedidos.pedidos'))

    # Mostrar todos los pedidos
    lista_pedidos = PedidosMySQL.mostrarPedido()
    return render_template(
        'pedidos.html',
        pedidos=lista_pedidos,
        active_page='pedidos',
        title="Pedidos"
    )

# API para obtener todos los pedidos
@api_pedidos.route('/api', methods=['GET'])
def api_obtener_pedidos():
    pedidos = PedidosMySQL.mostrarPedido()
    return jsonify(pedidos)

# API para obtener un pedido específico
@api_pedidos.route('/api/<int:id>', methods=['GET'])
def api_obtener_pedido(id):
    pedido = PedidosMySQL.obtenerPedido(id)  # Método que debe estar definido en tu modelo
    if pedido:
        return jsonify(pedido), 200
    else:
        return jsonify({"error": "Pedido no encontrado."}), 404

# API para modificar un pedido
@api_pedidos.route('/api/<int:id>', methods=['PUT'])
def api_modificar_pedido(id):
    data = request.json
    pedido_total = data.get('pedido_total')
    if pedido_total:
        if PedidosMySQL.modificarPedido(id, pedido_total):
            return jsonify({"message": "Pedido modificado correctamente."}), 200
        else:
            return jsonify({"error": "No se pudo modificar el pedido."}), 400
    else:
        return jsonify({"error": "Faltan datos para modificar el pedido."}), 400

# API para eliminar un pedido
@api_pedidos.route('/api/<int:id>', methods=['DELETE'])
def api_eliminar_pedido(id):
    if PedidosMySQL.eliminarPedido(id):
        return jsonify({"message": "Pedido eliminado correctamente."}), 200
    else:
        return jsonify({"error": "No se pudo eliminar el pedido."}), 400
