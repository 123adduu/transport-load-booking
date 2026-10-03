import uuid
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models import db, Vehicle, Driver, Load, Booking


assignments_bp = Blueprint(
    "assignments",
    __name__,
    url_prefix="/assignment"
)


def generate_booking_id():
    """Generate a human-readable unique booking ID."""

    date_part = datetime.utcnow().strftime("%Y%m%d")
    random_suffix = uuid.uuid4().hex[:4].upper()

    return f"BK-{date_part}-{random_suffix}"


@assignments_bp.route("/", methods=["GET", "POST"])
def assign():
    """Display and process vehicle/driver assignment."""

    error_message = None
    success_message = None

    if request.method == "POST":
        load_id_str = request.form.get(
            "load_id",
            ""
        ).strip()

        vehicle_id_str = request.form.get(
            "vehicle_id",
            ""
        ).strip()

        driver_id_str = request.form.get(
            "driver_id",
            ""
        ).strip()

        if not load_id_str:
            error_message = "Please select a load to assign."

        elif not vehicle_id_str:
            error_message = "Please select a vehicle."

        elif not driver_id_str:
            error_message = "Please select a driver."

        else:
            try:
                load_id = int(load_id_str)
                vehicle_id = int(vehicle_id_str)
                driver_id = int(driver_id_str)

                load = db.session.get(
                    Load,
                    load_id
                )

                vehicle = db.session.get(
                    Vehicle,
                    vehicle_id
                )

                driver = db.session.get(
                    Driver,
                    driver_id
                )

                if not load:
                    error_message = (
                        "Selected load does not exist."
                    )

                elif load.load_status != "Posted":
                    error_message = (
                        f"Load #{load.id} is already in "
                        f"{load.load_status} status and "
                        "cannot be assigned."
                    )

                elif not vehicle:
                    error_message = (
                        "Selected vehicle does not exist."
                    )

                elif vehicle.availability_status != "Available":
                    error_message = (
                        f"Vehicle {vehicle.vehicle_number} "
                        "is currently Unavailable."
                    )

                elif not driver:
                    error_message = (
                        "Selected driver does not exist."
                    )

                elif driver.availability_status != "Available":
                    error_message = (
                        f"Driver {driver.driver_name} "
                        "is currently Unavailable."
                    )

                elif vehicle.capacity < load.load_weight:
                    error_message = (
                        "Insufficient vehicle capacity: "
                        f"Vehicle capacity ({vehicle.capacity} tonnes) "
                        "is less than load weight "
                        f"({load.load_weight} tonnes)."
                    )

                else:
                    active_vehicle_booking = (
                        Booking.query.filter_by(
                            vehicle_id=vehicle.id,
                            status="Confirmed"
                        ).first()
                    )

                    if active_vehicle_booking:
                        error_message = (
                            f"Vehicle {vehicle.vehicle_number} "
                            "is already assigned to active booking "
                            f"{active_vehicle_booking.booking_id}."
                        )

                    active_driver_booking = (
                        Booking.query.filter_by(
                            driver_id=driver.id,
                            status="Confirmed"
                        ).first()
                    )

                    if (
                        not error_message
                        and active_driver_booking
                    ):
                        error_message = (
                            f"Driver {driver.driver_name} "
                            "is already assigned to active booking "
                            f"{active_driver_booking.booking_id}."
                        )

                if not error_message:
                    booking_id = generate_booking_id()

                    booking = Booking(
                        booking_id=booking_id,
                        load_id=load.id,
                        vehicle_id=vehicle.id,
                        driver_id=driver.id,
                        booking_date=datetime.utcnow(),
                        status="Confirmed"
                    )

                    vehicle.availability_status = "Unavailable"
                    driver.availability_status = "Unavailable"
                    load.load_status = "Assigned"

                    db.session.add(booking)
                    db.session.commit()

                    flash(
                        (
                            f"Booking {booking_id} successfully "
                            "created and confirmed!"
                        ),
                        "success"
                    )

                    return redirect(
                        url_for(
                            "bookings.booking_detail",
                            booking_id=booking_id
                        )
                    )

            except (ValueError, TypeError):
                error_message = (
                    "Invalid selection parameters."
                )

    posted_loads = (
        Load.query
        .filter_by(load_status="Posted")
        .order_by(Load.id.desc())
        .all()
    )

    available_vehicles = (
        Vehicle.query
        .filter_by(availability_status="Available")
        .order_by(Vehicle.vehicle_number)
        .all()
    )

    available_drivers = (
        Driver.query
        .filter_by(availability_status="Available")
        .order_by(Driver.driver_name)
        .all()
    )

    return render_template(
        "assignment.html",
        loads=posted_loads,
        vehicles=available_vehicles,
        drivers=available_drivers,
        error_message=error_message,
        success_message=success_message
    )