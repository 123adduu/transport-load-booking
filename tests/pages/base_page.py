from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    """Base Page Object providing explicit wait wrappers and reusable DOM interaction methods."""

    def __init__(self, driver, base_url="http://127.0.0.1:5001"):
        self.driver = driver
        self.base_url = base_url.rstrip('/')
        self.default_timeout = 10

    def open(self, path=""):
        target_url = f"{self.base_url}{path}" if path.startswith('/') else f"{self.base_url}/{path}"
        self.driver.get(target_url)

    def find(self, locator, timeout=None):
        t = timeout or self.default_timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator)
        )

    def find_visible(self, locator, timeout=None):
        t = timeout or self.default_timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def find_all(self, locator, timeout=None):
        t = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, t).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    def click(self, locator, timeout=None):
        element = self.find_visible(locator, timeout)
        WebDriverWait(self.driver, timeout or self.default_timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def type_text(self, locator, text, clear=True, timeout=None):
        element = self.find_visible(locator, timeout)
        if clear:
            element.clear()
        if text:
            element.send_keys(text)

    def select_by_value(self, locator, value, timeout=None):
        element = self.find_visible(locator, timeout)
        select = Select(element)
        select.select_by_value(str(value))

    def select_by_visible_text(self, locator, text, timeout=None):
        element = self.find_visible(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(str(text))

    def get_text(self, locator, timeout=None):
        try:
            element = self.find_visible(locator, timeout)
            return element.text.strip()
        except TimeoutException:
            return ""

    def is_displayed(self, locator, timeout=3):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title
