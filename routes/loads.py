import re
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Load, Booking

loads_bp = Blueprint('loads', __name__, url_prefix='/loads')

PHONE_REGEX = re.compile(r'^\d{10}$')

@loads_bp.route('/', methods=['GET', 'POST'])
def list_and_post():
    error_message = None
    success_message = None

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_phone = request.form.get('customer_phone', '').strip()
        material_type = request.form.get('material_type', '').strip()
        pickup_location = request.form.get('pickup_location', '').strip()
        destination = request.form.get('destination', '').strip()
        weight_str = request.form.get('load_weight', '').strip()
        required_vehicle_type = request.form.get('required_vehicle_type', '').strip()
        pickup_date_str = request.form.get('pickup_date', '').strip()
        price_str = request.form.get('offered_price', '').strip()

        # Validation
        if not customer_name:
            error_message = 'Customer name is required.'
        elif not customer_phone:
            error_message = 'Customer phone number is required.'
        elif not PHONE_REGEX.match(customer_phone):
            error_message = 'Customer phone number must contain exactly 10 digits.'
        elif not material_type:
            error_message = 'Material type is required.'
        elif not pickup_location:
            error_message = 'Pickup location is required.'
        elif not destination:
            error_message = 'Destination is required.'
        elif pickup_location.strip().lower() == destination.strip().lower():
            error_message = 'Pickup location and destination cannot be the same.'
        elif not weight_str:
            error_message = 'Load weight is required.'
        else:
            try:
                load_weight = float(weight_str)
                if load_weight <= 0:
                    error_message = 'Load weight must be a positive number greater than zero.'
            except ValueError:
                error_message = 'Load weight must be a valid number.'

        if not error_message:
            if not required_vehicle_type:
                error_message = 'Required vehicle type is required.'
            elif not pickup_date_str:
                error_message = 'Pickup date is required.'
            else:
                try:
                    pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
                    if pickup_date < date.today():
                        error_message = 'Pickup date cannot be in the past.'
                except ValueError:
                    error_message = 'Invalid pickup date format. Use YYYY-MM-DD.'

        if not error_message:
            if not price_str:
                error_message = 'Offered price is required.'
            else:
                try:
                    offered_price = float(price_str)
                    if offered_price <= 0:
                        error_message = 'Offered price must be greater than zero.'
                except ValueError:
                    error_message = 'Offered price must be a valid positive number.'

        if not error_message:
            new_load = Load(
                customer_name=customer_name,
                customer_phone=customer_phone,
                material_type=material_type,
                pickup_location=pickup_location,
                destination=destination,
                load_weight=float(weight_str),
                required_vehicle_type=required_vehicle_type,
                pickup_date=pickup_date,
                offered_price=float(price_str),
                load_status='Posted'
            )
            db.session.add(new_load)
            db.session.commit()
            success_message = f'Load for {customer_name} ({pickup_location} to {destination}) successfully posted!'
            flash(success_message, 'success')

    loads = Load.query.order_by(Load.id.desc()).all()
    return render_template(
        'loads.html',
        loads=loads,
        error_message=error_message,
        success_message=success_message,
        today_date=date.today().strftime('%Y-%m-%d')
    )

@loads_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    load = Load.query.get_or_404(id)
    error_message = None

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_phone = request.form.get('customer_phone', '').strip()
        material_type = request.form.get('material_type', '').strip()
        pickup_location = request.form.get('pickup_location', '').strip()
        destination = request.form.get('destination', '').strip()
        weight_str = request.form.get('load_weight', '').strip()
        required_vehicle_type = request.form.get('required_vehicle_type', '').strip()
        pickup_date_str = request.form.get('pickup_date', '').strip()
        price_str = request.form.get('offered_price', '').strip()
        load_status = request.form.get('load_status', load.load_status).strip()

        if not customer_name:
            error_message = 'Customer name is required.'
        elif not customer_phone or not PHONE_REGEX.match(customer_phone):
            error_message = 'Customer phone number must contain exactly 10 digits.'
        elif pickup_location.lower() == destination.lower():
            error_message = 'Pickup location and destination cannot be the same.'
        else:
            try:
                load_weight = float(weight_str)
                offered_price = float(price_str)
                pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
                if load_weight <= 0:
                    error_message = 'Load weight must be positive.'
                elif offered_price <= 0:
                    error_message = 'Offered price must be positive.'
                elif pickup_date < date.today():
                    error_message = 'Pickup date cannot be in the past.'
            except (ValueError, TypeError):
                error_message = 'Invalid numeric or date values provided.'

        if not error_message:
            load.customer_name = customer_name
            load.customer_phone = customer_phone
            load.material_type = material_type
            load.pickup_location = pickup_location
            load.destination = destination
            load.load_weight = float(weight_str)
            load.required_vehicle_type = required_vehicle_type
            load.pickup_date = pickup_date
            load.offered_price = float(price_str)
            load.load_status = load_status
            db.session.commit()
            flash(f'Load #{load.id} updated successfully!', 'success')
            return redirect(url_for('loads.list_and_post'))

    return render_template('load_edit.html', load=load, error_message=error_message)

@loads_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    load = Load.query.get_or_404(id)
    active_booking = Booking.query.filter_by(load_id=load.id, status='Confirmed').first()
    if active_booking:
        flash(f'Cannot delete load #{load.id} because it has an active booking ({active_booking.booking_id}).', 'danger')
    else:
        db.session.delete(load)
        db.session.commit()
        flash(f'Load #{load.id} deleted successfully.', 'info')
    return redirect(url_for('loads.list_and_post'))
