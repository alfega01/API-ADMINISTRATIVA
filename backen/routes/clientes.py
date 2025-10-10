from flask import Blueprint, request, jsonify
from models import db, Cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return jsonify([{
        "id": c.id, "nombre": c.nombre, "identificacion": c.identificacion,
        "telefono": c.telefono, "correo": c.correo, "direccion": c.direccion
    } for c in clientes])

@clientes_bp.route('/', methods=['POST'])
def crear_cliente():
    data = request.json
    c = Cliente(
        nombre=data.get('nombre'),
        identificacion=data.get('identificacion'),
        telefono=data.get('telefono'),
        correo=data.get('correo'),
        direccion=data.get('direccion')
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id}), 201

@clientes_bp.route('/<int:id>', methods=['PUT'])
def editar_cliente(id):
    c = Cliente.query.get_or_404(id)
    data = request.json
    c.nombre = data.get('nombre', c.nombre)
    c.identificacion = data.get('identificacion', c.identificacion)
    c.telefono = data.get('telefono', c.telefono)
    c.correo = data.get('correo', c.correo)
    c.direccion = data.get('direccion', c.direccion)
    db.session.commit()
    return jsonify({"ok": True})
