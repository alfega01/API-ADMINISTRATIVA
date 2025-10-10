from flask import Blueprint, request, jsonify
from models import db, Proveedor

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/', methods=['GET'])
def listar():
    p = Proveedor.query.order_by(Proveedor.id.desc()).all()
    return jsonify([{"id": x.id, "nombre": x.nombre, "nit": x.nit, "telefono": x.telefono, "correo": x.correo, "direccion": x.direccion} for x in p])

@proveedores_bp.route('/', methods=['POST'])
def crear():
    data = request.json
    prov = Proveedor(
        nombre=data.get('nombre'),
        nit=data.get('nit'),
        telefono=data.get('telefono'),
        correo=data.get('correo'),
        direccion=data.get('direccion')
    )
    db.session.add(prov)
    db.session.commit()
    return jsonify({"id": prov.id}), 201
