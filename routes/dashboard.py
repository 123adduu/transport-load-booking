from flask import Blueprint, render_template
from models import Vehicle, Driver, Load, Booking

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Dashboard homepage showing key fleet, driver, load, and booking metrics."""
    total_vehicles = Vehicle.query.count()
    available_vehicles = Vehicle.query.filter_by(availability_status='Available').count()
    
    total_drivers = Driver.query.count()
    available_drivers = Driver.query.filter_by(availability_status='Available').count()
    
    total_loads = Load.query.count()
    posted_loads = Load.query.filter_by(load_status='Posted').count()
    assigned_loads = Load.query.filter_by(load_status='Assigned').count()
    
    total_bookings = Booking.query.count()
    active_bookings = Booking.query.filter_by(status='Confirmed').count()
    cancelled_bookings = Booking.query.filter_by(status='Cancelled').count()
    
    recent_bookings = Booking.query.order_by(Booking.id.desc()).limit(5).all()
    recent_loads = Load.query.order_by(Load.id.desc()).limit(5).all()
    
    return render_template(
        'dashboard.html',
        total_vehicles=total_vehicles,
        available_vehicles=available_vehicles,
        total_drivers=total_drivers,
        available_drivers=available_drivers,
        total_loads=total_loads,
        posted_loads=posted_loads,
        assigned_loads=assigned_loads,
        total_bookings=total_bookings,
        active_bookings=active_bookings,
        cancelled_bookings=cancelled_bookings,
        recent_bookings=recent_bookings,
        recent_loads=recent_loads
    )
