from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage

class SearchPage(BasePage):
    """Page Object for Load Search and Multi-Parameter Filtering."""

    PATH = "/search/"

    PICKUP_LOCATION = (By.ID, 'search_pickup_location')
    DESTINATION = (By.ID, 'search_destination')
    MATERIAL_TYPE = (By.ID, 'search_material_type')
    VEHICLE_TYPE = (By.ID, 'search_vehicle_type')
    MIN_WEIGHT = (By.ID, 'search_min_weight')
    MAX_WEIGHT = (By.ID, 'search_max_weight')
    LOAD_STATUS = (By.ID, 'search_load_status')
    SEARCH_BUTTON = (By.ID, 'search_button')
    RESET_BUTTON = (By.ID, 'reset_search_button')

    SEARCH_RESULTS_TABLE = (By.ID, 'search_results_table')
    NO_LOADS_FOUND_MESSAGE = (By.ID, 'no_loads_found_message')

    def navigate(self):
        self.open(self.PATH)
        return self

    def search_loads(self, pickup="", destination="", material="", vehicle_type="", min_w="", max_w="", status=""):
        if pickup:
            self.type_text(self.PICKUP_LOCATION, pickup)
        if destination:
            self.type_text(self.DESTINATION, destination)
        if material:
            self.select_by_value(self.MATERIAL_TYPE, material)
        if vehicle_type:
            self.select_by_value(self.VEHICLE_TYPE, vehicle_type)
        if min_w:
            self.type_text(self.MIN_WEIGHT, str(min_w))
        if max_w:
            self.type_text(self.MAX_WEIGHT, str(max_w))
        if status:
            self.select_by_value(self.LOAD_STATUS, status)
        self.click(self.SEARCH_BUTTON)
        return self

    def has_no_matching_loads_message(self):
        return self.is_displayed(self.NO_LOADS_FOUND_MESSAGE)

    def is_results_table_displayed(self):
        return self.is_displayed(self.SEARCH_RESULTS_TABLE)

    def get_results_table_text(self):
        return self.get_text(self.SEARCH_RESULTS_TABLE)
