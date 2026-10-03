import os
import time
import socket
import threading
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from app import create_app
from models import db
from seed_database import seed_data


TEST_SERVER_PORT = 5001
TEST_BASE_URL = f"http://127.0.0.1:{TEST_SERVER_PORT}"

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

TEST_DB_PATH = os.path.join(
    PROJECT_ROOT,
    "instance",
    "test_transport.db"
).replace("\\", "/")


def is_port_in_use(port):
    """Check whether the specified local port is running."""

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as connection:
        return connection.connect_ex(
            ("127.0.0.1", port)
        ) == 0


@pytest.fixture(scope="session", autouse=True)
def live_server():
    """Start an isolated Flask server for Selenium tests."""

    if not is_port_in_use(TEST_SERVER_PORT):
        app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": (
                f"sqlite:///{TEST_DB_PATH}"
            )
        })

        with app.app_context():
            db.drop_all()
            db.create_all()
            seed_data(app)

        def run_flask():
            app.run(
                host="127.0.0.1",
                port=TEST_SERVER_PORT,
                debug=False,
                use_reloader=False
            )

        server_thread = threading.Thread(
            target=run_flask,
            daemon=True
        )
        server_thread.start()

        # Wait for a maximum of 10 seconds for Flask.
        start_time = time.time()

        while time.time() - start_time < 10:
            if is_port_in_use(TEST_SERVER_PORT):
                break

            time.sleep(0.2)

        if not is_port_in_use(TEST_SERVER_PORT):
            raise RuntimeError(
                "Flask test server failed to start on port 5001."
            )

    yield TEST_BASE_URL


@pytest.fixture(scope="function")
def driver(request):
    """Start visible Chrome and close it after each test."""

    chrome_options = Options()

    # Keep this commented so Chrome opens visibly.
    # chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-position=0,0")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    driver_instance = None

    try:
        # Selenium Manager automatically handles ChromeDriver.
        driver_instance = webdriver.Chrome(
            options=chrome_options
        )

    except Exception:
        # Fallback if Selenium Manager fails.
        from webdriver_manager.chrome import ChromeDriverManager

        service = Service(
            ChromeDriverManager().install()
        )

        driver_instance = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

    driver_instance.maximize_window()
    driver_instance.implicitly_wait(2)

    # Makes the driver available to the failure screenshot hook.
    request.node.driver = driver_instance

    try:
        # Selenium test executes here.
        yield driver_instance

    finally:
        # Keep Chrome visible for five seconds after the test.
        time.sleep(5)

        if driver_instance:
            driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a Selenium test fails."""

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_instance = getattr(
            item,
            "driver",
            None
        )

        if driver_instance:
            screenshots_dir = os.path.join(
                PROJECT_ROOT,
                "test_results",
                "screenshots"
            )

            os.makedirs(
                screenshots_dir,
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            clean_nodeid = (
                item.name
                .replace("/", "_")
                .replace(":", "_")
                .replace("[", "_")
                .replace("]", "_")
            )

            filename = (
                f"{clean_nodeid}_{timestamp}.png"
            )

            filepath = os.path.join(
                screenshots_dir,
                filename
            )

            try:
                driver_instance.save_screenshot(filepath)

                pytest_html = (
                    item.config.pluginmanager.getplugin("html")
                )

                if pytest_html:
                    extra = getattr(
                        report,
                        "extra",
                        []
                    )

                    extra.append(
                        pytest_html.extras.image(filepath)
                    )

                    report.extra = extra

            except Exception as error:
                print(
                    "Failed to capture failure screenshot: "
                    f"{error}"
                )