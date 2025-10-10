from .clientes import clientes_bp
from .proveedores import proveedores_bp
from .productos import productos_bp
from .facturas import facturas_bp
from .movimientos import movimientos_bp
from .config import config_bp

def register_routes(app):
    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
    app.register_blueprint(proveedores_bp, url_prefix='/api/proveedores')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')
    app.register_blueprint(facturas_bp, url_prefix='/api/facturas')
    app.register_blueprint(movimientos_bp, url_prefix='/api/movimientos')
    app.register_blueprint(config_bp, url_prefix='/api/config')
