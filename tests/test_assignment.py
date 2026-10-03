import os

from app import create_app
from models import Load, Vehicle, Driver
from tests.pages.assignment_page import AssignmentPage


# Find the project folder:
# C:\Users\ASUS\Desktop\transport_load_booking
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Create the correct absolute database path.
TEST_DB_PATH = os.path.join(
    PROJECT_ROOT,
    "instance",
    "test_transport.db"
).replace("\\", "/")

TEST_DATABASE_URI = f"sqlite:///{TEST_DB_PATH}"


def create_test_app():
    """Create an application connected to the Selenium test database."""

    return create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI
    })


class TestAssignment:
    """Automated tests for vehicle and driver assignment."""

    def test_insufficient_capacity_assignment_rejected(
        self,
        driver,
        live_server
    ):
        """Reject a vehicle whose capacity is less than load weight."""

        app = create_test_app()

        with app.app_context():
            heavy_load = Load.query.filter(
                Load.load_weight >= 20.0,
                Load.load_status == "Posted"
            ).first()

            small_vehicle = Vehicle.query.filter(
                Vehicle.capacity <= 5.0,
                Vehicle.availability_status == "Available"
            ).first()

            available_driver = Driver.query.filter_by(
                availability_status="Available"
            ).first()

            assert heavy_load is not None, (
                "Precondition failed: Heavy load not found"
            )

            assert small_vehicle is not None, (
                "Precondition failed: Small vehicle not found"
            )

            assert available_driver is not None, (
                "Precondition failed: Available driver not found"
            )

            load_id = heavy_load.id
            vehicle_id = small_vehicle.id
            driver_id = available_driver.id

        page = AssignmentPage(driver, live_server)
        page.navigate()

        page.assign(
            load_id=load_id,
            vehicle_id=vehicle_id,
            driver_id=driver_id
        )

        error_message = page.get_error_message()

        assert (
            "Insufficient vehicle capacity" in error_message
            or "less than load weight" in error_message.lower()
        ), (
            "Expected capacity error message, "
            f"but received: '{error_message}'"
        )

    def test_valid_vehicle_and_driver_assignment_success(
        self,
        driver,
        live_server
    ):
        """Assign a suitable vehicle and available driver successfully."""

        app = create_test_app()

        with app.app_context():
            load = Load.query.filter(
                Load.load_weight <= 10.0,
                Load.load_status == "Posted"
            ).first()

            vehicle = Vehicle.query.filter(
                Vehicle.capacity >= 15.0,
                Vehicle.availability_status == "Available"
            ).first()

            available_driver = Driver.query.filter_by(
                availability_status="Available"
            ).first()

            assert load is not None, (
                "Precondition failed: Suitable load not found"
            )

            assert vehicle is not None, (
                "Precondition failed: Suitable vehicle not found"
            )

            assert available_driver is not None, (
                "Precondition failed: Available driver not found"
            )

            load_id = load.id
            vehicle_id = vehicle.id
            driver_id = available_driver.id

        page = AssignmentPage(driver, live_server)
        page.navigate()

        page.assign(
            load_id=load_id,
            vehicle_id=vehicle_id,
            driver_id=driver_id
        )

        current_url = driver.current_url

        assert "/bookings/BK-" in current_url, (
            "Expected redirect to booking details, "
            f"but received URL: {current_url}"
        )