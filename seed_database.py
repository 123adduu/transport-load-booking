import os
import csv
import re
from datetime import datetime, date
from app import create_app
from models import db, Vehicle, Driver, Load

def clean_vehicle_number(v_num):
    if not v_num:
        return ''
    return re.sub(r'[\s\-]+', '', v_num.strip()).upper()

def seed_data(app=None):
    if app is None:
        app = create_app()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    datasets_dir = os.path.join(base_dir, 'datasets')

    vehicles_csv = os.path.join(datasets_dir, 'vehicles.csv')
    drivers_csv = os.path.join(datasets_dir, 'drivers.csv')
    loads_csv = os.path.join(datasets_dir, 'loads.csv')

    with app.app_context():
        # Ensure tables exist
        db.create_all()

        print("=" * 60)
        print("SEEDING TRANSPORT LOAD BOOKING DATABASE")
        print("=" * 60)

        # 1. Seed Vehicles
        veh_inserted = 0
        veh_skipped = 0
        if os.path.exists(vehicles_csv):
            with open(vehicles_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    v_num = clean_vehicle_number(row['vehicle_number'])
                    existing = Vehicle.query.filter_by(vehicle_number=v_num).first()
                    if existing:
                        veh_skipped += 1
                        continue

                    try:
                        reg_date = datetime.strptime(row['registration_date'], '%Y-%m-%d').date()
                    except (ValueError, KeyError):
                        reg_date = date.today()

                    v = Vehicle(
                        vehicle_number=v_num,
                        vehicle_type=row['vehicle_type'],
                        capacity=float(row['capacity']),
                        owner_name=row['owner_name'],
                        registration_date=reg_date,
                        availability_status=row.get('availability_status', 'Available')
                    )
                    db.session.add(v)
                    veh_inserted += 1
            db.session.commit()
            print(f"[Vehicles] Inserted: {veh_inserted}, Skipped/Duplicates: {veh_skipped}")
        else:
            print(f"[Vehicles] Warning: {vehicles_csv} not found.")

        # 2. Seed Drivers
        drv_inserted = 0
        drv_skipped = 0
        if os.path.exists(drivers_csv):
            with open(drivers_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    phone = row['phone_number'].strip()
                    licence = row['licence_number'].strip().upper()

                    existing = Driver.query.filter(
                        (Driver.phone_number == phone) | (Driver.licence_number == licence)
                    ).first()
                    if existing:
                        drv_skipped += 1
                        continue

                    try:
                        exp_date = datetime.strptime(row['licence_expiry_date'], '%Y-%m-%d').date()
                    except (ValueError, KeyError):
                        exp_date = date(2028, 12, 31)

                    d = Driver(
                        driver_name=row['driver_name'].strip(),
                        phone_number=phone,
                        licence_number=licence,
                        licence_expiry_date=exp_date,
                        availability_status=row.get('availability_status', 'Available')
                    )
                    db.session.add(d)
                    drv_inserted += 1
            db.session.commit()
            print(f"[Drivers]  Inserted: {drv_inserted}, Skipped/Duplicates: {drv_skipped}")
        else:
            print(f"[Drivers]  Warning: {drivers_csv} not found.")

        # 3. Seed Loads
        load_inserted = 0
        load_skipped = 0
        if os.path.exists(loads_csv):
            with open(loads_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    c_name = row['customer_name'].strip()
                    c_phone = row['customer_phone'].strip()
                    p_loc = row['pickup_location'].strip()
                    dest = row['destination'].strip()

                    # Check duplicate load
                    existing = Load.query.filter_by(
                        customer_name=c_name,
                        customer_phone=c_phone,
                        pickup_location=p_loc,
                        destination=dest
                    ).first()
                    if existing:
                        load_skipped += 1
                        continue

                    try:
                        p_date = datetime.strptime(row['pickup_date'], '%Y-%m-%d').date()
                    except (ValueError, KeyError):
                        p_date = date.today()

                    l = Load(
                        customer_name=c_name,
                        customer_phone=c_phone,
                        material_type=row['material_type'].strip(),
                        pickup_location=p_loc,
                        destination=dest,
                        load_weight=float(row['load_weight']),
                        required_vehicle_type=row['required_vehicle_type'].strip(),
                        pickup_date=p_date,
                        offered_price=float(row['offered_price']),
                        load_status=row.get('load_status', 'Posted')
                    )
                    db.session.add(l)
                    load_inserted += 1
            db.session.commit()
            print(f"[Loads]    Inserted: {load_inserted}, Skipped/Duplicates: {load_skipped}")
        else:
            print(f"[Loads]    Warning: {loads_csv} not found.")

        print("=" * 60)
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print(f"Total in DB: Vehicles={Vehicle.query.count()}, Drivers={Driver.query.count()}, Loads={Load.query.count()}")
        print("=" * 60)

if __name__ == '__main__':
    seed_data()
