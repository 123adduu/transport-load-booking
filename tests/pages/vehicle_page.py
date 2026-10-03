from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class VehiclePage(BasePage):
    """Page Object for vehicle registration and fleet listing."""

    PATH = "/vehicles/"

    VEHICLE_NUMBER = (By.ID, "vehicle_number")
    VEHICLE_TYPE = (By.ID, "vehicle_type")
    CAPACITY = (By.ID, "vehicle_capacity")
    OWNER_NAME = (By.ID, "owner_name")
    REGISTRATION_DATE = (By.ID, "registration_date")

    AVAILABILITY_STATUS = (
        By.ID,
        "vehicle_availability_status"
    )

    SUBMIT_BUTTON = (
        By.ID,
        "register_vehicle_button"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "#vehicle_success_message, .alert-success"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "#vehicle_error_message, .alert-danger"
    )

    VEHICLES_TABLE = (By.ID, "vehicles_table")

    def navigate(self):
        """Open the vehicle registration page."""
        self.open(self.PATH)
        return self

    def register_vehicle(
        self,
        vehicle_number,
        vehicle_type,
        capacity,
        owner_name,
        reg_date="2026-09-01",
        status="Available"
    ):
        """Complete and submit the vehicle registration form."""

        self.type_text(
            self.VEHICLE_NUMBER,
            vehicle_number
        )

        if vehicle_type:
            vehicle_dropdown = WebDriverWait(
                self.driver,
                5
            ).until(
                EC.element_to_be_clickable(
                    self.VEHICLE_TYPE
                )
            )

            Select(
                vehicle_dropdown
            ).select_by_visible_text(vehicle_type)

        self.type_text(
            self.CAPACITY,
            str(capacity)
        )

        self.type_text(
            self.OWNER_NAME,
            owner_name
        )

        if reg_date:
            date_input = WebDriverWait(
                self.driver,
                5
            ).until(
                EC.presence_of_element_located(
                    self.REGISTRATION_DATE
                )
            )

            self.driver.execute_script(
                """
                arguments[0].value = arguments[1];

                arguments[0].dispatchEvent(
                    new Event('input', {bubbles: true})
                );

                arguments[0].dispatchEvent(
                    new Event('change', {bubbles: true})
                );
                """,
                date_input,
                reg_date
            )

        if status:
            status_dropdown = WebDriverWait(
                self.driver,
                5
            ).until(
                EC.element_to_be_clickable(
                    self.AVAILABILITY_STATUS
                )
            )

            Select(
                status_dropdown
            ).select_by_visible_text(status)

        submit_button = WebDriverWait(
            self.driver,
            5
        ).until(
            EC.presence_of_element_located(
                self.SUBMIT_BUTTON
            )
        )

        # Move the button away from anything that may cover it.
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: 'instant',
                block: 'center'
            });
            """,
            submit_button
        )

        try:
            clickable_button = WebDriverWait(
                self.driver,
                5
            ).until(
                EC.element_to_be_clickable(
                    self.SUBMIT_BUTTON
                )
            )

            clickable_button.click()

        except ElementClickInterceptedException:
            # Fallback when a fixed element overlaps the button.
            self.driver.execute_script(
                "arguments[0].click();",
                submit_button
            )

        return self

    def get_success_message(self):
        """Return the displayed success message."""

        try:
            message = WebDriverWait(
                self.driver,
                5
            ).until(
                EC.visibility_of_element_located(
                    self.SUCCESS_MESSAGE
                )
            )

            return message.text.strip()

        except Exception:
            return ""

    def get_error_message(self):
        """Return the displayed validation/error message."""

        try:
            message = WebDriverWait(
                self.driver,
                5
            ).until(
                EC.visibility_of_element_located(
                    self.ERROR_MESSAGE
                )
            )

            return message.text.strip()

        except Exception:
            return ""

    def is_vehicle_in_table(self, vehicle_number):
        """Check whether a vehicle is present in the fleet table."""

        table_text = self.get_text(
            self.VEHICLES_TABLE
        )

        return (
            vehicle_number.upper()
            in table_text.upper()
        )