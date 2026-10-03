from app import create_app
from models import Vehicle, Driver, Load, Booking

def test_endpoints():
    app = create_app()
    client = app.test_client()

    with app.app_context():
        # 1. Dashboard
        r = client.get('/')
        assert r.status_code == 200, f"Dashboard failed: {r.status_code}"
        assert b"Logistics Operations Dashboard" in r.data
        print("[PASS] GET / (Dashboard)")

        # 2. Vehicles
        r = client.get('/vehicles/')
        assert r.status_code == 200, f"Vehicles failed: {r.status_code}"
        assert b"Registered Commercial Vehicles" in r.data
        print("[PASS] GET /vehicles/")

        # 3. Drivers
        r = client.get('/drivers/')
        assert r.status_code == 200, f"Drivers failed: {r.status_code}"
        assert b"Registered Drivers" in r.data
        print("[PASS] GET /drivers/")

        # 4. Loads
        r = client.get('/loads/')
        assert r.status_code == 200, f"Loads failed: {r.status_code}"
        assert b"Freight Cargo Consignments" in r.data
        print("[PASS] GET /loads/")

        # 5. Search
        r = client.get('/search/?pickup_location=Mangaluru')
        assert r.status_code == 200, f"Search failed: {r.status_code}"
        assert b"Mangaluru" in r.data
        print("[PASS] GET /search/ (With results)")

        r = client.get('/search/?pickup_location=NonExistentCityXYZ')
        assert r.status_code == 200
        assert b"No matching loads found" in r.data
        print("[PASS] GET /search/ (No matching loads found check)")

        # 6. Assignment
        r = client.get('/assignment/')
        assert r.status_code == 200, f"Assignment failed: {r.status_code}"
        assert b"assignment_heading" in r.data
        print("[PASS] GET /assignment/")

        # 7. Bookings
        r = client.get('/bookings/')
        assert r.status_code == 200, f"Bookings failed: {r.status_code}"
        assert b"Transport Bookings Registry" in r.data
        print("[PASS] GET /bookings/")

        # 8. Import
        r = client.get('/import/')
        assert r.status_code == 200, f"Import failed: {r.status_code}"
        assert b"Import CSV Datasets" in r.data
        print("[PASS] GET /import/")

    print("\nALL FLASK ENDPOINTS VERIFIED AND WORKING PROPERLY!")

if __name__ == '__main__':
    test_endpoints()
