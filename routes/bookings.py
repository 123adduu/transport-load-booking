from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Booking, Vehicle, Driver, Load

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bookings_bp.route('/', methods=['GET'])
def list_bookings():
    status_filter = request.args.get('status', '').strip()
    query = Booking.query.order_by(Booking.id.desc())

    if status_filter:
        query = query.filter_by(status=status_filter)

    bookings = query.all()
    return render_template(
        'bookings.html',
        bookings=bookings,
        current_filter=status_filter
    )

@bookings_bp.route('/<booking_id>', methods=['GET'])
def booking_detail(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first_or_404()
    return render_template('booking_detail.html', booking=booking)

@bookings_bp.route('/cancel/<int:id>', methods=['POST'])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)

    if booking.status == 'Cancelled':
        flash(f'Booking {booking.booking_id} is already cancelled.', 'warning')
        return redirect(url_for('bookings.list_bookings'))

    # Revert vehicle and driver to Available
    if booking.vehicle:
        booking.vehicle.availability_status = 'Available'
    if booking.driver:
        booking.driver.availability_status = 'Available'
    if booking.load:
        booking.load.load_status = 'Posted'

    booking.status = 'Cancelled'
    db.session.commit()

    flash(f'Booking {booking.booking_id} has been cancelled. Vehicle and Driver are now Available.', 'success')
    return redirect(url_for('bookings.booking_detail', booking_id=booking.booking_id))
