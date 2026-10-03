import pytest
from tests.utils.csv_reader import read_csv_data
from tests.pages.vehicle_page import VehiclePage

test_cases = read_csv_data('vehicle_registration_test_data.csv')

class TestVehicleRegistration:
    """Data-Driven Tests for Vehicle Registration Module."""

    @pytest.mark.parametrize('data', test_cases, ids=[tc['test_case_id'] for tc in test_cases])
    def test_vehicle_registration_data_driven(self, driver, live_server, data):
        page = VehiclePage(driver, live_server)
        page.navigate()

        page.register_vehicle(
            vehicle_number=data['vehicle_number'],
            vehicle_type=data['vehicle_type'],
            capacity=data['capacity'],
            owner_name=data['owner_name'],
            reg_date=data['registration_date'],
            status=data['availability_status']
        )

        expected_res = data['expected_result']
        expected_msg = data['expected_message']

        if expected_res == 'Success':
            success_text = page.get_success_message()
            assert expected_msg in success_text or 'successfully registered' in success_text.lower(), \
                f"Expected success message containing '{expected_msg}', got '{success_text}'"
            # Verify vehicle appears in table
            if data['vehicle_number']:
                assert page.is_vehicle_in_table(data['vehicle_number']), \
                    f"Vehicle {data['vehicle_number']} not found in vehicles table."
        else:
            error_text = page.get_error_message()
            assert expected_msg.lower() in error_text.lower(), \
                f"Expected error message containing '{expected_msg}', got '{error_text}'"
