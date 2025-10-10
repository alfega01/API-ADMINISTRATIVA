from flask import Blueprint, request, jsonify
from models import db, Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def listar():
    productos = Producto.query.order_by(Producto.nombre).all()
    return jsonify([{
        "id": p.id, "codigo": p.codigo, "nombre": p.nombre, "categoria": p.categoria,
        "cantidad": p.cantidad, "precio": str(p.precio)
    } for p in productos])

@productos_bp.route('/', methods=['POST'])
def crear():
    d = request.json
    p = Producto(codigo=d.get('codigo'), nombre=d['nombre'], categoria=d.get('categoria'), cantidad=d.get('cantidad',0), precio=d.get('precio',0))
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id}), 201
