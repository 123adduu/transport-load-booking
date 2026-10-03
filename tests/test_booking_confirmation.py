import os
from datetime import datetime

from app import create_app
from models import db, Booking, Load, Vehicle, Driver
from routes.assignments import generate_booking_id
from tests.pages.booking_page import BookingPage


# Absolute project directory.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Absolute path to the Selenium test database.
TEST_DB_PATH = os.path.join(
    PROJECT_ROOT,
    "instance",
    "test_transport.db"
).replace("\\", "/")

TEST_DATABASE_URI = f"sqlite:///{TEST_DB_PATH}"


def create_test_app():
    """Create an app connected to the Selenium test database."""

    return create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI
    })


class TestBookingConfirmation:
    """Automated tests for the booking-confirmation voucher."""

    def test_booking_confirmation_voucher_details(
        self,
        driver,
        live_server
    ):
        """Verify that the booking voucher displays correct details."""

        app = create_test_app()

        with app.app_context():
            # Use an existing confirmed booking when available.
            booking = Booking.query.filter_by(
                status="Confirmed"
            ).first()

            # Create a confirmed booking when none exists.
            if booking is None:
                load = Load.query.filter_by(
                    load_status="Posted"
                ).first()

                vehicle = Vehicle.query.filter_by(
                    availability_status="Available"
                ).first()

                available_driver = Driver.query.filter_by(
                    availability_status="Available"
                ).first()

                assert load is not None, (
                    "Precondition failed: Posted load not found"
                )

                assert vehicle is not None, (
                    "Precondition failed: Available vehicle not found"
                )

                assert available_driver is not None, (
                    "Precondition failed: Available driver not found"
                )

                booking_id = generate_booking_id()

                booking = Booking(
                    booking_id=booking_id,
                    load_id=load.id,
                    vehicle_id=vehicle.id,
                    driver_id=available_driver.id,
                    booking_date=datetime.utcnow(),
                    status="Confirmed"
                )

                vehicle.availability_status = "Unavailable"
                available_driver.availability_status = "Unavailable"
                load.load_status = "Assigned"

                db.session.add(booking)
                db.session.commit()

            # Store values before leaving the application context.
            booking_id = booking.booking_id
            customer_name = booking.load.customer_name
            vehicle_number = booking.vehicle.vehicle_number
            driver_name = booking.driver.driver_name

        page = BookingPage(
            driver,
            live_server
        )

        page.open_booking_detail(booking_id)

        displayed_booking_id = (
            page.get_displayed_booking_id()
        )

        displayed_status = (
            page.get_booking_status()
        )

        page_source = driver.page_source

        assert displayed_booking_id == booking_id, (
            "Booking ID does not match. "
            f"Expected '{booking_id}', "
            f"but displayed '{displayed_booking_id}'."
        )

        assert displayed_status == "Confirmed", (
            "Booking status should be 'Confirmed', "
            f"but displayed '{displayed_status}'."
        )

        assert customer_name in page_source, (
            f"Customer '{customer_name}' "
            "was not found in the voucher."
        )

        assert vehicle_number in page_source, (
            f"Vehicle '{vehicle_number}' "
            "was not found in the voucher."
        )

        assert driver_name in page_source, (
            f"Driver '{driver_name}' "
            "was not found in the voucher."
        )