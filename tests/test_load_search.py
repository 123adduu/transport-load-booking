import pytest
from tests.utils.csv_reader import read_csv_data
from tests.pages.search_page import SearchPage

test_cases = read_csv_data('load_search_test_data.csv')

class TestLoadSearch:
    """Data-Driven Tests for Load Search Module."""

    @pytest.mark.parametrize('data', test_cases, ids=[tc['test_case_id'] for tc in test_cases])
    def test_load_search_data_driven(self, driver, live_server, data):
        page = SearchPage(driver, live_server)
        page.navigate()

        page.search_loads(
            pickup=data.get('pickup_location', ''),
            destination=data.get('destination', ''),
            material=data.get('material_type', ''),
            vehicle_type=data.get('required_vehicle_type', ''),
            min_w=data.get('min_weight', ''),
            max_w=data.get('max_weight', ''),
            status=data.get('load_status', '')
        )

        expected_res = data['expected_result']

        if expected_res == 'Results_Found':
            assert page.is_results_table_displayed(), "Expected search results table to be displayed."
            results_text = page.get_results_table_text()
            expected_keyword = data.get('expected_message', '')
            if expected_keyword and expected_keyword not in ['10 to 20']:
                assert expected_keyword.lower() in results_text.lower(), \
                    f"Expected keyword '{expected_keyword}' in search results."
        else:
            # Must display 'No matching loads found' message with ID #no_loads_found_message
            assert page.has_no_matching_loads_message(), \
                "Expected 'No matching loads found' message (#no_loads_found_message) to be displayed."
