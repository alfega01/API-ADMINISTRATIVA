from flask import Blueprint, request, jsonify
from models import db, Factura, FacturaLinea, Producto, Movimiento
from datetime import datetime

facturas_bp = Blueprint('facturas', __name__)

@facturas_bp.route('/', methods=['GET'])
def listar():
    tipo = request.args.get('tipo')  # compra o venta
    q = Factura.query
    if tipo:
        q = q.filter_by(tipo=tipo)
    facturas = q.order_by(Factura.fecha.desc()).all()
    res = []
    for f in facturas:
        lineas = []
        for l in f.lineas:
            lineas.append({
                "id": l.id,
                "producto_id": l.producto_id,
                "descripcion": l.descripcion,
                "cantidad": l.cantidad,
                "precio_unitario": str(l.precio_unitario)
            })
        res.append({
            "id": f.id,
            "tipo": f.tipo,
            "numero": f.numero,
            "fecha": f.fecha.isoformat(),
            "cliente_id": f.cliente_id,
            "proveedor_id": f.proveedor_id,
            "total": str(f.total),
            "lineas": lineas
        })
    return jsonify(res)

@facturas_bp.route('/', methods=['POST'])
def crear():
    data = request.json
    fecha = datetime.fromisoformat(data.get('fecha')).date() if data.get('fecha') else datetime.utcnow().date()
    f = Factura(tipo=data['tipo'], numero=data.get('numero'), fecha=fecha,
                cliente_id=data.get('cliente_id'), proveedor_id=data.get('proveedor_id'),
                notas=data.get('notas'))
    # Agregar lineas
    total = 0
    for linea in data.get('lineas', []):
        prod_id = linea.get('producto_id')
        cantidad = int(linea.get('cantidad',1))
        precio_unitario = float(linea.get('precio_unitario',0))
        fl = FacturaLinea(producto_id=prod_id, descripcion=linea.get('descripcion'), cantidad=cantidad, precio_unitario=precio_unitario)
        f.lineas.append(fl)
        total += cantidad * precio_unitario
        # Ajuste de stock si es venta o compra
        if prod_id:
            prod = Producto.query.get(prod_id)
            if prod:
                if data['tipo'] == 'venta':
                    prod.cantidad = max(0, prod.cantidad - cantidad)
                else:
                    prod.cantidad = prod.cantidad + cantidad
    f.total = total
    db.session.add(f)
    db.session.commit()
    # Registro de movimiento
    mov = Movimiento(tipo=data['tipo'], referencia_id=f.id, descripcion=f"Factura {f.tipo} #{f.id}", monto=total)
    db.session.add(mov)
    db.session.commit()
    return jsonify({"id": f.id}), 201
