import os
from datetime import datetime

from app import create_app
from models import db, Booking, Load, Vehicle, Driver
from routes.assignments import generate_booking_id
from tests.pages.booking_page import BookingPage

from selenium.webdriver.support.ui import WebDriverWait


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
    """Create an application connected to the test database."""

    return create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI
    })


class TestBookingCancellation:
    """Automated tests for the booking-cancellation flow."""

    def test_booking_cancellation_restores_availability(
        self,
        driver,
        live_server
    ):
        """Cancel a booking and restore all related availability."""

        app = create_test_app()

        # Create a separate confirmed booking for this test.
        with app.app_context():
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

            test_booking = Booking(
                booking_id=booking_id,
                load_id=load.id,
                vehicle_id=vehicle.id,
                driver_id=available_driver.id,
                booking_date=datetime.utcnow(),
                status="Confirmed"
            )

            # Mark the related records as assigned/unavailable.
            vehicle.availability_status = "Unavailable"
            available_driver.availability_status = "Unavailable"
            load.load_status = "Assigned"

            db.session.add(test_booking)
            db.session.commit()

            vehicle_id = vehicle.id
            driver_id = available_driver.id
            load_id = load.id

        page = BookingPage(
            driver,
            live_server
        )

        page.open_booking_detail(booking_id)

        # Verify the initial booking status.
        initial_status = page.get_booking_status()

        assert initial_status == "Confirmed", (
            "Initial booking status should be 'Confirmed', "
            f"but displayed '{initial_status}'."
        )

        # Cancel the booking through Selenium.
        page.cancel_booking()

        # Wait for the updated booking page to display Cancelled.
        WebDriverWait(
            driver,
            10
        ).until(
            lambda browser: (
                page.get_booking_status() == "Cancelled"
            )
        )

        updated_status = page.get_booking_status()

        assert updated_status == "Cancelled", (
            "Booking status did not change to 'Cancelled'. "
            f"Displayed status: '{updated_status}'."
        )

        # Confirm that database statuses were restored.
        with app.app_context():
            cancelled_booking = Booking.query.filter_by(
                booking_id=booking_id
            ).first()

            assert cancelled_booking is not None, (
                "Cancelled booking was not found in the database."
            )

            assert cancelled_booking.status == "Cancelled", (
                "Database booking status should be 'Cancelled', "
                f"but was '{cancelled_booking.status}'."
            )

            restored_vehicle = db.session.get(
                Vehicle,
                vehicle_id
            )

            restored_driver = db.session.get(
                Driver,
                driver_id
            )

            restored_load = db.session.get(
                Load,
                load_id
            )

            assert restored_vehicle is not None
            assert restored_driver is not None
            assert restored_load is not None

            assert (
                restored_vehicle.availability_status
                == "Available"
            ), (
                "Vehicle status should be 'Available', "
                f"but was "
                f"'{restored_vehicle.availability_status}'."
            )

            assert (
                restored_driver.availability_status
                == "Available"
            ), (
                "Driver status should be 'Available', "
                f"but was "
                f"'{restored_driver.availability_status}'."
            )

            assert restored_load.load_status == "Posted", (
                "Load status should be 'Posted', "
                f"but was '{restored_load.load_status}'."
            )