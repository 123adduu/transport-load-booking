import os
import csv

def get_dataset_path(filename):
    """Returns absolute path to a CSV file inside the datasets directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, 'datasets', filename)

def read_csv_data(filename):
    """Reads a CSV file and returns a list of dictionaries."""
    filepath = get_dataset_path(filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset CSV file not found at: {filepath}")
    
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def get_test_cases_by_type(filename, test_type=None):
    """Returns test cases filtered optionally by test_type ('Positive', 'Negative', 'Boundary')."""
    rows = read_csv_data(filename)
    if test_type:
        return [r for r in rows if r.get('test_type', '').lower() == test_type.lower()]
    return rows
