from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage

class BookingPage(BasePage):
    """Page Object for Booking Confirmation Voucher and Bookings Registry Table."""

    PATH = "/bookings/"

    BOOKINGS_TABLE = (By.ID, 'bookings_table')
    BOOKING_ID_DISPLAY = (By.ID, 'booking_id_display')
    STATUS_BADGE = (By.ID, 'booking_status_badge')
    CANCEL_BUTTON = (By.ID, 'cancel_booking_button')
    CUSTOMER_NAME = (By.ID, 'booking_customer_name')
    VEHICLE_NUMBER = (By.ID, 'booking_vehicle_number')
    DRIVER_NAME = (By.ID, 'booking_driver_name')

    def navigate(self):
        self.open(self.PATH)
        return self

    def open_booking_detail(self, booking_id):
        self.open(f"/bookings/{booking_id}")
        return self

    def get_displayed_booking_id(self):
        return self.get_text(self.BOOKING_ID_DISPLAY)

    def get_booking_status(self):
        return self.get_text(self.STATUS_BADGE)

    def cancel_booking(self):
        self.click(self.CANCEL_BUTTON)
        # Handle alert dialog if any
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception:
            pass
        return self

    def is_booking_in_table(self, booking_id):
        table_text = self.get_text(self.BOOKINGS_TABLE)
        return booking_id in table_text
