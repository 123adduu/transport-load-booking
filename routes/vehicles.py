import re
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Vehicle, Booking

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/vehicles')

INDIAN_VEHICLE_NO_REGEX = re.compile(r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$')

def normalize_vehicle_number(v_num):
    """Normalize vehicle number by removing spaces/hyphens and uppercasing."""
    if not v_num:
        return ''
    return re.sub(r'[\s\-]+', '', v_num.strip()).upper()

@vehicles_bp.route('/', methods=['GET', 'POST'])
def list_and_register():
    error_message = None
    success_message = None

    if request.method == 'POST':
        raw_number = request.form.get('vehicle_number', '')
        vehicle_type = request.form.get('vehicle_type', '').strip()
        capacity_str = request.form.get('capacity', '').strip()
        owner_name = request.form.get('owner_name', '').strip()
        reg_date_str = request.form.get('registration_date', '').strip()
        availability_status = request.form.get('availability_status', 'Available').strip()

        vehicle_number = normalize_vehicle_number(raw_number)

        # Validations
        if not vehicle_number:
            error_message = 'Vehicle number is required.'
        elif not INDIAN_VEHICLE_NO_REGEX.match(vehicle_number):
            error_message = 'Invalid Indian vehicle registration number format (e.g., KA19AB1234).'
        elif not vehicle_type or vehicle_type not in ['Truck', 'Mini Truck', 'Trailer', 'Pickup']:
            error_message = 'Please select a valid vehicle type (Truck, Mini Truck, Trailer, or Pickup).'
        elif not capacity_str:
            error_message = 'Vehicle capacity is required.'
        else:
            try:
                capacity = float(capacity_str)
                if capacity <= 0:
                    error_message = 'Capacity must be greater than zero tonnes.'
            except ValueError:
                error_message = 'Capacity must be a valid positive number.'

        if not error_message and not owner_name:
            error_message = 'Owner name is required.'

        reg_date = date.today()
        if not error_message and reg_date_str:
            try:
                reg_date = datetime.strptime(reg_date_str, '%Y-%m-%d').date()
            except ValueError:
                error_message = 'Invalid registration date format. Use YYYY-MM-DD.'

        # Check duplicate
        if not error_message:
            existing = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
            if existing:
                error_message = f'Vehicle number {vehicle_number} is already registered.'

        if not error_message:
            new_vehicle = Vehicle(
                vehicle_number=vehicle_number,
                vehicle_type=vehicle_type,
                capacity=float(capacity_str),
                owner_name=owner_name,
                registration_date=reg_date,
                availability_status=availability_status if availability_status in ['Available', 'Unavailable'] else 'Available'
            )
            db.session.add(new_vehicle)
            db.session.commit()
            success_message = f'Vehicle {vehicle_number} successfully registered!'
            flash(success_message, 'success')

    vehicles = Vehicle.query.order_by(Vehicle.id.desc()).all()
    return render_template(
        'vehicles.html',
        vehicles=vehicles,
        error_message=error_message,
        success_message=success_message
    )

@vehicles_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    vehicle = Vehicle.query.get_or_404(id)
    error_message = None
    success_message = None

    if request.method == 'POST':
        raw_number = request.form.get('vehicle_number', '')
        vehicle_type = request.form.get('vehicle_type', '').strip()
        capacity_str = request.form.get('capacity', '').strip()
        owner_name = request.form.get('owner_name', '').strip()
        availability_status = request.form.get('availability_status', vehicle.availability_status).strip()

        vehicle_number = normalize_vehicle_number(raw_number)

        if not vehicle_number:
            error_message = 'Vehicle number is required.'
        elif not INDIAN_VEHICLE_NO_REGEX.match(vehicle_number):
            error_message = 'Invalid Indian vehicle registration number format.'
        elif not capacity_str:
            error_message = 'Capacity is required.'
        else:
            try:
                capacity = float(capacity_str)
                if capacity <= 0:
                    error_message = 'Capacity must be greater than zero.'
            except ValueError:
                error_message = 'Capacity must be a valid number.'

        if not error_message and not owner_name:
            error_message = 'Owner name is required.'

        if not error_message:
            duplicate = Vehicle.query.filter(Vehicle.vehicle_number == vehicle_number, Vehicle.id != id).first()
            if duplicate:
                error_message = f'Vehicle number {vehicle_number} is already in use by another vehicle.'

        if not error_message:
            vehicle.vehicle_number = vehicle_number
            vehicle.vehicle_type = vehicle_type
            vehicle.capacity = float(capacity_str)
            vehicle.owner_name = owner_name
            vehicle.availability_status = availability_status
            db.session.commit()
            flash(f'Vehicle {vehicle.vehicle_number} updated successfully!', 'success')
            return redirect(url_for('vehicles.list_and_register'))

    return render_template('vehicle_edit.html', vehicle=vehicle, error_message=error_message)

@vehicles_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    vehicle = Vehicle.query.get_or_404(id)
    # Check if vehicle has active confirmed booking
    active_booking = Booking.query.filter_by(vehicle_id=vehicle.id, status='Confirmed').first()
    if active_booking:
        flash(f'Cannot delete vehicle {vehicle.vehicle_number} because it has an active booking ({active_booking.booking_id}).', 'danger')
    else:
        db.session.delete(vehicle)
        db.session.commit()
        flash(f'Vehicle {vehicle.vehicle_number} deleted successfully.', 'info')
    return redirect(url_for('vehicles.list_and_register'))
