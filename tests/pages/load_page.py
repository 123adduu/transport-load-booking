import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class LoadPage(BasePage):
    """Page Object for Load Posting and Consignment Management."""

    PATH = "/loads/"

    CUSTOMER_NAME = (
        By.ID,
        "customer_name"
    )

    CUSTOMER_PHONE = (
        By.ID,
        "customer_phone"
    )

    MATERIAL_TYPE = (
        By.ID,
        "material_type"
    )

    PICKUP_LOCATION = (
        By.ID,
        "pickup_location"
    )

    DESTINATION = (
        By.ID,
        "destination"
    )

    LOAD_WEIGHT = (
        By.ID,
        "load_weight"
    )

    REQUIRED_VEHICLE_TYPE = (
        By.ID,
        "required_vehicle_type"
    )

    PICKUP_DATE = (
        By.ID,
        "pickup_date"
    )

    OFFERED_PRICE = (
        By.ID,
        "offered_price"
    )

    SUBMIT_BUTTON = (
        By.ID,
        "post_load_button"
    )

    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        "#load_success_message, .alert-success"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "#load_error_message, .alert-danger"
    )

    LOADS_TABLE = (
        By.ID,
        "loads_table"
    )

    def navigate(self):
        """Open the load-posting page."""

        self.open(self.PATH)

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.CUSTOMER_NAME
            )
        )

        return self

    def set_input_using_javascript(
        self,
        locator,
        value,
        remove_maxlength=False
    ):
        """Set an input value using JavaScript."""

        element = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                locator
            )
        )

        if remove_maxlength:
            self.driver.execute_script(
                "arguments[0].removeAttribute('maxlength');",
                element
            )

        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];

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

    def select_option(
        self,
        locator,
        option
    ):
        """Select an option using text first and value as fallback."""

        dropdown = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                locator
            )
        )

        try:
            Select(
                dropdown
            ).select_by_visible_text(
                str(option)
            )

        except Exception:
            Select(
                dropdown
            ).select_by_value(
                str(option)
            )

    def post_load(
        self,
        customer_name,
        customer_phone,
        material_type,
        pickup_location,
        destination,
        weight,
        vehicle_type,
        pickup_date,
        price
    ):
        """Fill and submit the load-posting form."""

        if customer_name is not None:
            self.type_text(
                self.CUSTOMER_NAME,
                str(customer_name)
            )

        if customer_phone is not None:
            # Remove maxlength so invalid long-phone tests can
            # reach the backend validation without truncation.
            self.set_input_using_javascript(
                self.CUSTOMER_PHONE,
                customer_phone,
                remove_maxlength=True
            )

        if material_type:
            self.select_option(
                self.MATERIAL_TYPE,
                material_type
            )

        if pickup_location is not None:
            self.type_text(
                self.PICKUP_LOCATION,
                str(pickup_location)
            )

        if destination is not None:
            self.type_text(
                self.DESTINATION,
                str(destination)
            )

        if weight is not None:
            self.type_text(
                self.LOAD_WEIGHT,
                str(weight)
            )

        if vehicle_type:
            self.select_option(
                self.REQUIRED_VEHICLE_TYPE,
                vehicle_type
            )

        if pickup_date:
            # HTML date fields require YYYY-MM-DD.
            self.set_input_using_javascript(
                self.PICKUP_DATE,
                pickup_date
            )

        if price is not None:
            self.type_text(
                self.OFFERED_PRICE,
                str(price)
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

        except (
            ElementClickInterceptedException,
            TimeoutException
        ):
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

    def is_load_in_table(self, customer_name):
        """Check whether the customer load appears in the table."""

        try:
            table = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.LOADS_TABLE
                )
            )

            return (
                str(customer_name).lower()
                in table.text.lower()
            )

        except TimeoutException:
            return False  