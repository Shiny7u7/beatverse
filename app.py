from flask import Flask
from routes.usuarios import api_usuarios
from routes.roles import api_roles
from routes.paises import api_paises
from routes.ciudades import api_ciudades
from routes.estados import api_estados
from routes.bitacoras import api_bitacora
from routes.clientes import api_clientes
from routes.pedidos import api_pedidos
from routes.tablas import api_tablas
from routes.permisos import api_permisos

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Registro de blueprints
app.register_blueprint(api_usuarios, url_prefix='/usuarios')
app.register_blueprint(api_roles, url_prefix='/roles')
app.register_blueprint(api_paises, url_prefix='/pais')
app.register_blueprint(api_ciudades, url_prefix='/ciudades')
app.register_blueprint(api_estados, url_prefix='/estados')
app.register_blueprint(api_pedidos, url_prefix='/pedidos')
app.register_blueprint(api_bitacora, url_prefix='/bitacora')
app.register_blueprint(api_clientes, url_prefix='/clientes')
app.register_blueprint(api_tablas, url_prefix='/tabla')
app.register_blueprint(api_permisos, url_prefix='/permisos')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
