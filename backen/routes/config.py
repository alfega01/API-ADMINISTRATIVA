from flask import Blueprint, jsonify, request
from models import Configuracion, db

config_bp = Blueprint('config', __name__)

@config_bp.route('/', methods=['GET'])
def listar():
    keys = Configuracion.query.all()
    return jsonify({k.clave: k.valor for k in keys})

@config_bp.route('/<clave>', methods=['PUT'])
def actualizar(clave):
    data = request.json
    valor = data.get('valor')
    cfg = Configuracion.query.filter_by(clave=clave).first()
    if cfg:
        cfg.valor = valor
    else:
        cfg = Configuracion(clave=clave, valor=valor)
        db.session.add(cfg)
    db.session.commit()
    return jsonify({"ok": True})
