import pytest
from tests.utils.csv_reader import read_csv_data
from tests.pages.load_page import LoadPage

test_cases = read_csv_data('load_posting_test_data.csv')

class TestLoadPosting:
    """Data-Driven Tests for Load Posting Module."""

    @pytest.mark.parametrize('data', test_cases, ids=[tc['test_case_id'] for tc in test_cases])
    def test_load_posting_data_driven(self, driver, live_server, data):
        page = LoadPage(driver, live_server)
        page.navigate()

        page.post_load(
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
            material_type=data['material_type'],
            pickup_location=data['pickup_location'],
            destination=data['destination'],
            weight=data['load_weight'],
            vehicle_type=data['required_vehicle_type'],
            pickup_date=data['pickup_date'],
            price=data['offered_price']
        )

        expected_res = data['expected_result']
        expected_msg = data['expected_message']

        if expected_res == 'Success':
            success_text = page.get_success_message()
            assert expected_msg in success_text or 'successfully posted' in success_text.lower(), \
                f"Expected success message containing '{expected_msg}', got '{success_text}'"
            if data['customer_name']:
                assert page.is_load_in_table(data['customer_name']), \
                    f"Load for customer '{data['customer_name']}' not found in loads table."
        else:
            error_text = page.get_error_message()
            assert expected_msg.lower() in error_text.lower(), \
                f"Expected error message containing '{expected_msg}', got '{error_text}'"
