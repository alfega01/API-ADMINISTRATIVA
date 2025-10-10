from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(120))
    rol = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    identificacion = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    facturas = db.relationship('Factura', backref='cliente', lazy=True)

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    nit = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True)
    nombre = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(120))
    cantidad = db.Column(db.Integer, default=0)
    precio = db.Column(db.Numeric(12,2), default=0.00)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('compra','venta'), nullable=False)
    numero = db.Column(db.String(100))
    fecha = db.Column(db.Date, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=True)
    total = db.Column(db.Numeric(12,2), default=0.00)
    notas = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    lineas = db.relationship('FacturaLinea', backref='factura', lazy=True, cascade="all, delete-orphan")

class FacturaLinea(db.Model):
    __tablename__ = 'factura_linea'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=True)
    descripcion = db.Column(db.String(500))
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Numeric(12,2), default=0.00)
    # subtotal can be computed on the fly in responses

class Movimiento(db.Model):
    __tablename__ = 'movimiento'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    referencia_id = db.Column(db.Integer)
    descripcion = db.Column(db.String(500))
    monto = db.Column(db.Numeric(12,2), default=0.00)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
