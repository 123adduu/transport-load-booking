from flask import Blueprint, render_template, request
from models import Load

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/', methods=['GET'])
def search_loads():
    pickup = request.args.get('pickup_location', '').strip()
    destination = request.args.get('destination', '').strip()
    material = request.args.get('material_type', '').strip()
    vehicle_type = request.args.get('required_vehicle_type', '').strip()
    min_weight_str = request.args.get('min_weight', '').strip()
    max_weight_str = request.args.get('max_weight', '').strip()
    status = request.args.get('load_status', '').strip()

    has_searched = bool(request.args)

    query = Load.query

    if pickup:
        query = query.filter(Load.pickup_location.ilike(f'%{pickup}%'))
    if destination:
        query = query.filter(Load.destination.ilike(f'%{destination}%'))
    if material:
        query = query.filter(Load.material_type.ilike(f'%{material}%'))
    if vehicle_type:
        query = query.filter(Load.required_vehicle_type == vehicle_type)
    if min_weight_str:
        try:
            min_weight = float(min_weight_str)
            query = query.filter(Load.load_weight >= min_weight)
        except ValueError:
            pass
    if max_weight_str:
        try:
            max_weight = float(max_weight_str)
            query = query.filter(Load.load_weight <= max_weight)
        except ValueError:
            pass
    if status:
        query = query.filter(Load.load_status == status)

    loads = query.order_by(Load.id.desc()).all()

    return render_template(
        'search.html',
        loads=loads,
        has_searched=has_searched,
        pickup=pickup,
        destination=destination,
        material=material,
        vehicle_type=vehicle_type,
        min_weight=min_weight_str,
        max_weight=max_weight_str,
        status=status
    )
