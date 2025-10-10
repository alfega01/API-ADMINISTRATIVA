from flask import Blueprint, jsonify
from models import Movimiento

movimientos_bp = Blueprint('movimientos', __name__)

@movimientos_bp.route('/', methods=['GET'])
def listar():
    movs = Movimiento.query.order_by(Movimiento.creado_en.desc()).limit(100).all()
    return jsonify([{"id": m.id, "tipo": m.tipo, "referencia_id": m.referencia_id, "descripcion": m.descripcion, "monto": str(m.monto), "creado_en": m.creado_en.isoformat()} for m in movs])
