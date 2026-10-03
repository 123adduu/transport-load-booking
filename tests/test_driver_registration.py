import pytest

from tests.utils.csv_reader import read_csv_data
from tests.pages.driver_page import DriverPage


test_cases = read_csv_data(
    "driver_registration_test_data.csv"
)


class TestDriverRegistration:
    """Data-driven tests for the Driver Registration module."""

    @pytest.mark.parametrize(
        "data",
        test_cases,
        ids=[
            test_case["test_case_id"]
            for test_case in test_cases
        ]
    )
    def test_driver_registration_data_driven(
        self,
        driver,
        live_server,
        data
    ):
        page = DriverPage(driver, live_server)
        page.navigate()

        # Diagnostic information from the CSV file.
        print(
            f"\nTest case: {data['test_case_id']}"
        )
        print(
            "DATE READ FROM CSV:",
            repr(data["licence_expiry_date"])
        )
        print(
            "PHONE READ FROM CSV:",
            repr(data["phone_number"])
        )
        print(
            "LICENCE READ FROM CSV:",
            repr(data["licence_number"])
        )

        page.register_driver(
            driver_name=data["driver_name"],
            phone_number=data["phone_number"],
            licence_number=data["licence_number"],
            expiry_date=data["licence_expiry_date"],
            status=data["availability_status"]
        )

        expected_result = (
            data["expected_result"].strip()
        )

        expected_message = (
            data["expected_message"].strip()
        )

        if expected_result.lower() == "success":
            success_text = page.get_success_message()
            error_text = page.get_error_message()

            print(
                f"Expected message: {expected_message}"
            )
            print(
                f"Actual success message: {success_text}"
            )
            print(
                f"Actual error message: {error_text}"
            )

            assert (
                expected_message.lower()
                in success_text.lower()
                or "successfully registered"
                in success_text.lower()
            ), (
                "Expected success message containing "
                f"'{expected_message}', but received "
                f"success='{success_text}', "
                f"error='{error_text}'"
            )

            if data["driver_name"].strip():
                assert page.is_driver_in_table(
                    data["driver_name"]
                ), (
                    f"Driver '{data['driver_name']}' "
                    "was not found in the drivers table."
                )

        else:
            error_text = page.get_error_message()
            success_text = page.get_success_message()

            print(
                f"Expected error: {expected_message}"
            )
            print(
                f"Actual error message: {error_text}"
            )
            print(
                f"Actual success message: {success_text}"
            )

            assert (
                expected_message.lower()
                in error_text.lower()
            ), (
                "Expected error message containing "
                f"'{expected_message}', but received "
                f"error='{error_text}', "
                f"success='{success_text}'"
            )