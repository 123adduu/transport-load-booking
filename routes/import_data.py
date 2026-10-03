import csv
import io
import re
from datetime import datetime, date
from flask import Blueprint, render_template, request, flash
from models import db, Vehicle, Driver, Load

import_data_bp = Blueprint('import_data', __name__, url_prefix='/import')

REQUIRED_VEHICLE_COLS = {'vehicle_number', 'vehicle_type', 'capacity', 'owner_name', 'registration_date', 'availability_status'}
REQUIRED_DRIVER_COLS = {'driver_name', 'phone_number', 'licence_number', 'licence_expiry_date', 'availability_status'}
REQUIRED_LOAD_COLS = {'customer_name', 'customer_phone', 'material_type', 'pickup_location', 'destination', 'load_weight', 'required_vehicle_type', 'pickup_date', 'offered_price', 'load_status'}

INDIAN_VEHICLE_NO_REGEX = re.compile(r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$')
PHONE_REGEX = re.compile(r'^\d{10}$')

@import_data_bp.route('/', methods=['GET', 'POST'])
def import_csv():
    error_message = None
    success_message = None
    imported_count = 0
    skipped_count = 0
    errors_list = []

    if request.method == 'POST':
        dataset_type = request.form.get('dataset_type', '').strip()
        csv_file = request.files.get('csv_file')

        if not dataset_type or dataset_type not in ['vehicles', 'drivers', 'loads']:
            error_message = 'Please select a valid dataset type to import (Vehicles, Drivers, or Loads).'
        elif not csv_file or csv_file.filename == '':
            error_message = 'Please choose a CSV file to upload.'
        elif not csv_file.filename.lower().endswith('.csv'):
            error_message = 'Uploaded file must be a CSV file (.csv).'
        else:
            try:
                content = csv_file.read().decode('utf-8-sig')
                reader = csv.DictReader(io.StringIO(content))
                fieldnames = set(reader.fieldnames or [])

                if dataset_type == 'vehicles':
                    missing = REQUIRED_VEHICLE_COLS - fieldnames
                    if missing:
                        error_message = f"Missing required columns in CSV: {', '.join(sorted(missing))}"
                    else:
                        for row_idx, row in enumerate(reader, start=2):
                            v_num = re.sub(r'[\s\-]+', '', row.get('vehicle_number', '').strip()).upper()
                            v_type = row.get('vehicle_type', '').strip()
                            cap_str = row.get('capacity', '').strip()
                            owner = row.get('owner_name', '').strip()
                            reg_date_str = row.get('registration_date', '').strip()
                            status = row.get('availability_status', 'Available').strip()

                            if not v_num or not INDIAN_VEHICLE_NO_REGEX.match(v_num):
                                errors_list.append(f"Row {row_idx}: Invalid vehicle number format '{v_num}'.")
                                skipped_count += 1
                                continue
                            try:
                                cap = float(cap_str)
                                if cap <= 0:
                                    raise ValueError()
                            except (ValueError, TypeError):
                                errors_list.append(f"Row {row_idx}: Invalid capacity '{cap_str}'.")
                                skipped_count += 1
                                continue

                            # Duplicate check
                            if Vehicle.query.filter_by(vehicle_number=v_num).first():
                                skipped_count += 1
                                continue

                            try:
                                reg_date = datetime.strptime(reg_date_str, '%Y-%m-%d').date() if reg_date_str else date.today()
                            except ValueError:
                                reg_date = date.today()

                            new_v = Vehicle(
                                vehicle_number=v_num,
                                vehicle_type=v_type if v_type in ['Truck', 'Mini Truck', 'Trailer', 'Pickup'] else 'Truck',
                                capacity=cap,
                                owner_name=owner or 'Transport Fleet',
                                registration_date=reg_date,
                                availability_status=status if status in ['Available', 'Unavailable'] else 'Available'
                            )
                            db.session.add(new_v)
                            imported_count += 1
                        db.session.commit()

                elif dataset_type == 'drivers':
                    missing = REQUIRED_DRIVER_COLS - fieldnames
                    if missing:
                        error_message = f"Missing required columns in CSV: {', '.join(sorted(missing))}"
                    else:
                        for row_idx, row in enumerate(reader, start=2):
                            d_name = row.get('driver_name', '').strip()
                            phone = row.get('phone_number', '').strip()
                            licence = row.get('licence_number', '').strip().upper()
                            exp_str = row.get('licence_expiry_date', '').strip()
                            status = row.get('availability_status', 'Available').strip()

                            if not d_name or not PHONE_REGEX.match(phone) or not licence:
                                errors_list.append(f"Row {row_idx}: Missing required fields or invalid phone '{phone}'.")
                                skipped_count += 1
                                continue

                            try:
                                exp_date = datetime.strptime(exp_str, '%Y-%m-%d').date()
                            except ValueError:
                                errors_list.append(f"Row {row_idx}: Invalid expiry date '{exp_str}'.")
                                skipped_count += 1
                                continue

                            if Driver.query.filter((Driver.phone_number == phone) | (Driver.licence_number == licence)).first():
                                skipped_count += 1
                                continue

                            new_d = Driver(
                                driver_name=d_name,
                                phone_number=phone,
                                licence_number=licence,
                                licence_expiry_date=exp_date,
                                availability_status=status if status in ['Available', 'Unavailable'] else 'Available'
                            )
                            db.session.add(new_d)
                            imported_count += 1
                        db.session.commit()

                elif dataset_type == 'loads':
                    missing = REQUIRED_LOAD_COLS - fieldnames
                    if missing:
                        error_message = f"Missing required columns in CSV: {', '.join(sorted(missing))}"
                    else:
                        for row_idx, row in enumerate(reader, start=2):
                            c_name = row.get('customer_name', '').strip()
                            c_phone = row.get('customer_phone', '').strip()
                            mat = row.get('material_type', '').strip()
                            pickup = row.get('pickup_location', '').strip()
                            dest = row.get('destination', '').strip()
                            w_str = row.get('load_weight', '').strip()
                            req_v = row.get('required_vehicle_type', '').strip()
                            p_date_str = row.get('pickup_date', '').strip()
                            price_str = row.get('offered_price', '').strip()
                            l_status = row.get('load_status', 'Posted').strip()

                            if not c_name or not PHONE_REGEX.match(c_phone) or not mat or not pickup or not dest:
                                errors_list.append(f"Row {row_idx}: Incomplete load info or invalid phone.")
                                skipped_count += 1
                                continue

                            if pickup.lower() == dest.lower():
                                errors_list.append(f"Row {row_idx}: Pickup and destination cannot be the same.")
                                skipped_count += 1
                                continue

                            try:
                                weight = float(w_str)
                                price = float(price_str)
                                p_date = datetime.strptime(p_date_str, '%Y-%m-%d').date()
                                if weight <= 0 or price <= 0:
                                    raise ValueError()
                            except (ValueError, TypeError):
                                errors_list.append(f"Row {row_idx}: Invalid weight, price, or date.")
                                skipped_count += 1
                                continue

                            new_l = Load(
                                customer_name=c_name,
                                customer_phone=c_phone,
                                material_type=mat,
                                pickup_location=pickup,
                                destination=dest,
                                load_weight=weight,
                                required_vehicle_type=req_v or 'Truck',
                                pickup_date=p_date,
                                offered_price=price,
                                load_status=l_status if l_status in ['Posted', 'Assigned', 'Completed', 'Cancelled'] else 'Posted'
                            )
                            db.session.add(new_l)
                            imported_count += 1
                        db.session.commit()

                if not error_message:
                    success_message = f"CSV import finished: {imported_count} records imported, {skipped_count} skipped/duplicates."
                    flash(success_message, 'success')

            except Exception as e:
                error_message = f"Error processing CSV: {str(e)}"

    return render_template(
        'import_data.html',
        error_message=error_message,
        success_message=success_message,
        imported_count=imported_count,
        skipped_count=skipped_count,
        errors_list=errors_list
    )
