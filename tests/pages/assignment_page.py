import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class AssignmentPage(BasePage):
    """Page Object for Vehicle and Driver Assignment."""

    PATH = "/assignment/"

    LOAD_SELECT = (
        By.ID,
        "assignment_load_id"
    )

    VEHICLE_SELECT = (
        By.ID,
        "assignment_vehicle_id"
    )

    DRIVER_SELECT = (
        By.ID,
        "assignment_driver_id"
    )

    ASSIGN_BUTTON = (
        By.ID,
        "assign_button"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "#assignment_success_message, .alert-success"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "#assignment_error_message, .alert-danger"
    )

    def navigate(self):
        """Open the assignment page."""

        self.open(self.PATH)

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.LOAD_SELECT
            )
        )

        return self

    def select_dropdown_value(self, locator, value):
        """Wait for and select a dropdown option by its value."""

        dropdown = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(locator)
        )

        Select(dropdown).select_by_value(
            str(value)
        )

    def assign(self, load_id, vehicle_id, driver_id):
        """Select a load, vehicle and driver, then submit."""

        if load_id is not None:
            self.select_dropdown_value(
                self.LOAD_SELECT,
                load_id
            )

        if vehicle_id is not None:
            self.select_dropdown_value(
                self.VEHICLE_SELECT,
                vehicle_id
            )

        if driver_id is not None:
            self.select_dropdown_value(
                self.DRIVER_SELECT,
                driver_id
            )

        assign_button = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.ASSIGN_BUTTON
            )
        )

        # Move the button into the visible area.
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            assign_button
        )

        time.sleep(0.5)

        try:
            clickable_button = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.element_to_be_clickable(
                    self.ASSIGN_BUTTON
                )
            )

            clickable_button.click()

        except ElementClickInterceptedException:
            # Fallback when another element blocks the button.
            self.driver.execute_script(
                "arguments[0].click();",
                assign_button
            )

        return self

    def get_error_message(self):
        """Return the visible assignment error message."""

        try:
            message = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.ERROR_MESSAGE
                )
            )

            return message.text.strip()

        except TimeoutException:
            return ""

    def get_success_message(self):
        """Return the visible assignment success message."""

        try:
            message = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.SUCCESS_MESSAGE
                )
            )

            return message.text.strip()

        except TimeoutException:
            return ""