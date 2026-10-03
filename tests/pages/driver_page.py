import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class DriverPage(BasePage):
    """Page Object for Driver Registration and Driver Listing."""

    PATH = "/drivers/"

    DRIVER_NAME = (
        By.ID,
        "driver_name"
    )

    PHONE = (
        By.ID,
        "driver_phone"
    )

    LICENCE = (
        By.ID,
        "driver_licence"
    )

    EXPIRY_DATE = (
        By.ID,
        "licence_expiry_date"
    )

    AVAILABILITY_STATUS = (
        By.ID,
        "driver_availability_status"
    )

    SUBMIT_BUTTON = (
        By.ID,
        "register_driver_button"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "#driver_success_message, .alert-success"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "#driver_error_message, .alert-danger"
    )

    DRIVERS_TABLE = (
        By.ID,
        "drivers_table"
    )

    def navigate(self):
        """Open the driver registration page."""

        self.open(self.PATH)

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.DRIVER_NAME
            )
        )

        return self

    def set_input_using_javascript(
        self,
        locator,
        value
    ):
        """Set an input value and trigger input/change events."""

        element = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                locator
            )
        )

        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];

            arguments[0].dispatchEvent(
                new Event(
                    'input',
                    {bubbles: true}
                )
            );

            arguments[0].dispatchEvent(
                new Event(
                    'change',
                    {bubbles: true}
                )
            );
            """,
            element,
            str(value)
        )

        return element

    def set_phone_number(self, phone_number):
        """
        Set the complete phone number.

        The maxlength attribute and input event can truncate an
        11-digit negative-test value. This method bypasses that
        browser-side restriction so backend validation can be tested.
        """

        phone_input = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.PHONE
            )
        )

        self.driver.execute_script(
            """
            arguments[0].removeAttribute('maxlength');
            arguments[0].value = arguments[1];

            arguments[0].dispatchEvent(
                new Event(
                    'change',
                    {bubbles: true}
                )
            );
            """,
            phone_input,
            str(phone_number)
        )

        return phone_input

    def register_driver(
        self,
        driver_name,
        phone_number,
        licence_number,
        expiry_date,
        status="Available"
    ):
        """Fill and submit the driver-registration form."""

        if driver_name:
            self.type_text(
                self.DRIVER_NAME,
                driver_name
            )

        if phone_number is not None:
            self.set_phone_number(
                phone_number
            )

        if licence_number:
            self.type_text(
                self.LICENCE,
                licence_number
            )

        if expiry_date:
            # HTML date fields require YYYY-MM-DD.
            self.set_input_using_javascript(
                self.EXPIRY_DATE,
                expiry_date
            )

        if status:
            status_dropdown = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.element_to_be_clickable(
                    self.AVAILABILITY_STATUS
                )
            )

            try:
                Select(
                    status_dropdown
                ).select_by_visible_text(
                    status
                )

            except Exception:
                Select(
                    status_dropdown
                ).select_by_value(
                    status
                )

        submit_button = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.SUBMIT_BUTTON
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            submit_button
        )

        time.sleep(0.5)

        try:
            clickable_button = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.element_to_be_clickable(
                    self.SUBMIT_BUTTON
                )
            )

            clickable_button.click()

        except ElementClickInterceptedException:
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
                10
            ).until(
                EC.visibility_of_element_located(
                    self.SUCCESS_MESSAGE
                )
            )

            return message.text.strip()

        except TimeoutException:
            return ""

    def get_error_message(self):
        """Return the displayed validation error."""

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

    def is_driver_in_table(self, driver_name):
        """Check whether the driver appears in the table."""

        try:
            table = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.DRIVERS_TABLE
                )
            )

            return (
                driver_name.lower()
                in table.text.lower()
            )

        except TimeoutException:
            return False