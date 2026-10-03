import re
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Driver, Booking

drivers_bp = Blueprint('drivers', __name__, url_prefix='/drivers')

PHONE_REGEX = re.compile(r'^\d{10}$')

@drivers_bp.route('/', methods=['GET', 'POST'])
def list_and_register():
    error_message = None
    success_message = None

    if request.method == 'POST':
        driver_name = request.form.get('driver_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        licence_number = request.form.get('licence_number', '').strip().upper()
        expiry_date_str = request.form.get('licence_expiry_date', '').strip()
        availability_status = request.form.get('availability_status', 'Available').strip()

        # Validation
        if not driver_name:
            error_message = 'Driver name is required.'
        elif not phone_number:
            error_message = 'Phone number is required.'
        elif not PHONE_REGEX.match(phone_number):
            error_message = 'Phone number must contain exactly 10 digits.'
        elif not licence_number:
            error_message = 'Driving licence number is required.'
        elif not expiry_date_str:
            error_message = 'Licence expiry date is required.'
        else:
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                if expiry_date <= date.today():
                    error_message = 'Licence expiry date must be a future date.'
            except ValueError:
                error_message = 'Invalid licence expiry date format. Use YYYY-MM-DD.'

        # Uniqueness checks
        if not error_message:
            dup_phone = Driver.query.filter_by(phone_number=phone_number).first()
            if dup_phone:
                error_message = f'Phone number {phone_number} is already registered to another driver.'

        if not error_message:
            dup_licence = Driver.query.filter_by(licence_number=licence_number).first()
            if dup_licence:
                error_message = f'Driving licence number {licence_number} is already registered.'

        if not error_message:
            new_driver = Driver(
                driver_name=driver_name,
                phone_number=phone_number,
                licence_number=licence_number,
                licence_expiry_date=expiry_date,
                availability_status=availability_status if availability_status in ['Available', 'Unavailable'] else 'Available'
            )
            db.session.add(new_driver)
            db.session.commit()
            success_message = f'Driver {driver_name} successfully registered!'
            flash(success_message, 'success')

    drivers = Driver.query.order_by(Driver.id.desc()).all()
    return render_template(
        'drivers.html',
        drivers=drivers,
        error_message=error_message,
        success_message=success_message
    )

@drivers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    driver = Driver.query.get_or_404(id)
    error_message = None

    if request.method == 'POST':
        driver_name = request.form.get('driver_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        licence_number = request.form.get('licence_number', '').strip().upper()
        expiry_date_str = request.form.get('licence_expiry_date', '').strip()
        availability_status = request.form.get('availability_status', driver.availability_status).strip()

        if not driver_name:
            error_message = 'Driver name is required.'
        elif not phone_number or not PHONE_REGEX.match(phone_number):
            error_message = 'Phone number must contain exactly 10 digits.'
        elif not licence_number:
            error_message = 'Licence number is required.'
        elif not expiry_date_str:
            error_message = 'Expiry date is required.'
        else:
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                if expiry_date <= date.today():
                    error_message = 'Licence expiry date must be a future date.'
            except ValueError:
                error_message = 'Invalid expiry date.'

        if not error_message:
            dup_phone = Driver.query.filter(Driver.phone_number == phone_number, Driver.id != id).first()
            if dup_phone:
                error_message = f'Phone number {phone_number} is already in use.'

        if not error_message:
            dup_lic = Driver.query.filter(Driver.licence_number == licence_number, Driver.id != id).first()
            if dup_lic:
                error_message = f'Licence number {licence_number} is already in use.'

        if not error_message:
            driver.driver_name = driver_name
            driver.phone_number = phone_number
            driver.licence_number = licence_number
            driver.licence_expiry_date = expiry_date
            driver.availability_status = availability_status
            db.session.commit()
            flash(f'Driver {driver.driver_name} updated successfully!', 'success')
            return redirect(url_for('drivers.list_and_register'))

    return render_template('driver_edit.html', driver=driver, error_message=error_message)

@drivers_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    driver = Driver.query.get_or_404(id)
    active_booking = Booking.query.filter_by(driver_id=driver.id, status='Confirmed').first()
    if active_booking:
        flash(f'Cannot delete driver {driver.driver_name} because they have an active booking ({active_booking.booking_id}).', 'danger')
    else:
        db.session.delete(driver)
        db.session.commit()
        flash(f'Driver {driver.driver_name} deleted successfully.', 'info')
    return redirect(url_for('drivers.list_and_register'))
