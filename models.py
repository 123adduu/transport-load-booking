from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):
    """Represents a commercial transport vehicle."""
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    vehicle_type = db.Column(db.String(20), nullable=False)  # Truck, Mini Truck, Trailer, Pickup
    capacity = db.Column(db.Float, nullable=False)  # In tonnes (> 0)
    owner_name = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.Date, nullable=False, default=date.today)
    availability_status = db.Column(db.String(20), nullable=False, default='Available')  # Available, Unavailable

    # Relationship to bookings
    bookings = db.relationship('Booking', back_populates='vehicle', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_number': self.vehicle_number,
            'vehicle_type': self.vehicle_type,
            'capacity': self.capacity,
            'owner_name': self.owner_name,
            'registration_date': self.registration_date.strftime('%Y-%m-%d') if self.registration_date else '',
            'availability_status': self.availability_status
        }


class Driver(db.Model):
    """Represents a commercial driver."""
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False, index=True)  # Exactly 10 digits
    licence_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    licence_expiry_date = db.Column(db.Date, nullable=False)  # Must be future date
    availability_status = db.Column(db.String(20), nullable=False, default='Available')  # Available, Unavailable

    # Relationship to bookings
    bookings = db.relationship('Booking', back_populates='driver', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'driver_name': self.driver_name,
            'phone_number': self.phone_number,
            'licence_number': self.licence_number,
            'licence_expiry_date': self.licence_expiry_date.strftime('%Y-%m-%d') if self.licence_expiry_date else '',
            'availability_status': self.availability_status
        }


class Load(db.Model):
    """Represents a freight cargo/load posted by a customer."""
    __tablename__ = 'loads'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)  # Exactly 10 digits
    material_type = db.Column(db.String(50), nullable=False)
    pickup_location = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    load_weight = db.Column(db.Float, nullable=False)  # In tonnes (> 0)
    required_vehicle_type = db.Column(db.String(20), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)  # Cannot be in past
    offered_price = db.Column(db.Float, nullable=False)  # Strictly positive
    load_status = db.Column(db.String(20), nullable=False, default='Posted')  # Posted, Assigned, Completed, Cancelled

    # Relationship to booking
    booking = db.relationship('Booking', back_populates='load', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'material_type': self.material_type,
            'pickup_location': self.pickup_location,
            'destination': self.destination,
            'load_weight': self.load_weight,
            'required_vehicle_type': self.required_vehicle_type,
            'pickup_date': self.pickup_date.strftime('%Y-%m-%d') if self.pickup_date else '',
            'offered_price': self.offered_price,
            'load_status': self.load_status
        }


class Booking(db.Model):
    """Represents a confirmed assignment/booking connecting a load, vehicle, and driver."""
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(30), unique=True, nullable=False, index=True)
    load_id = db.Column(db.Integer, db.ForeignKey('loads.id'), nullable=False, unique=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Confirmed')  # Confirmed, Cancelled

    # Relationships
    load = db.relationship('Load', back_populates='booking')
    vehicle = db.relationship('Vehicle', back_populates='bookings')
    driver = db.relationship('Driver', back_populates='bookings')

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'load_id': self.load_id,
            'vehicle_id': self.vehicle_id,
            'driver_id': self.driver_id,
            'booking_date': self.booking_date.strftime('%Y-%m-%d %H:%M:%S') if self.booking_date else '',
            'status': self.status,
            'load': self.load.to_dict() if self.load else None,
            'vehicle': self.vehicle.to_dict() if self.vehicle else None,
            'driver': self.driver.to_dict() if self.driver else None
        }
