import csv
import os

datasets_dir = r'C:\Users\ASUS\.gemini\antigravity\scratch\transport_load_booking\datasets'
project_dir = r'C:\Users\ASUS\.gemini\antigravity\scratch\transport_load_booking'
os.makedirs(datasets_dir, exist_ok=True)

# 1. vehicles.csv (35 records >= 30)
vehicles = [
    ("KA19AB1234", "Truck", 16.0, "Mangaluru Coastal Carriers", "2024-01-15", "Available"),
    ("KA19CD5678", "Mini Truck", 3.5, "Canara Express Cargo", "2024-02-10", "Available"),
    ("KA20EF9012", "Trailer", 28.0, "Udupi Heavy Haulers", "2023-11-05", "Available"),
    ("KA01GH3456", "Pickup", 1.8, "Bengaluru Metro Logistics", "2024-03-01", "Available"),
    ("KA09IJ7890", "Truck", 14.5, "Mysuru Royal Transports", "2023-09-20", "Available"),
    ("KA14KL2345", "Mini Truck", 4.0, "Malnad Freight Movers", "2024-04-12", "Available"),
    ("KA13MN6789", "Truck", 18.0, "Hassan Agro Logistics", "2023-12-18", "Available"),
    ("KA25OP1234", "Trailer", 32.0, "North Karnataka Heavy Transit", "2023-08-14", "Available"),
    ("KA22QR5678", "Truck", 15.0, "Belagavi Border Cargo", "2024-02-25", "Available"),
    ("KA19ST9012", "Pickup", 2.0, "Kudla Goods Express", "2024-05-02", "Available"),
    ("KA01UV3456", "Truck", 20.0, "Silicon City Translines", "2023-10-11", "Available"),
    ("KA09WX7890", "Trailer", 30.0, "Chamundi Heavy Fleet", "2023-07-29", "Available"),
    ("KA20YZ1234", "Mini Truck", 3.2, "Karavali Fast Freight", "2024-03-18", "Available"),
    ("KA14AB5678", "Truck", 12.5, "Sahyadri Roadways", "2023-11-22", "Available"),
    ("KA13CD9012", "Pickup", 1.5, "Hassan Coffee Carriers", "2024-04-30", "Available"),
    ("KA25EF3456", "Truck", 16.5, "Hubballi Junction Logistics", "2024-01-08", "Available"),
    ("KA22GH7890", "Trailer", 26.0, "Kittur Express Haulage", "2023-09-03", "Available"),
    ("KA19IJ1234", "Truck", 10.0, "Panambur Port Logistics", "2024-02-14", "Available"),
    ("KA01KL5678", "Mini Truck", 4.5, "Whitefield Distribution", "2024-05-15", "Available"),
    ("KA09MN9012", "Pickup", 2.2, "Heritage Cargo Lines", "2024-03-22", "Available"),
    ("KA20OP3456", "Truck", 22.0, "Udupi Highway Transporters", "2023-12-01", "Available"),
    ("KA14QR7890", "Trailer", 35.0, "Sharavathi Heavy Movers", "2023-06-19", "Available"),
    ("KA13ST1234", "Mini Truck", 3.8, "Hassan Potato Express", "2024-04-05", "Available"),
    ("KA25UV5678", "Pickup", 1.7, "Dharwad Pedha Cargo", "2024-05-20", "Available"),
    ("KA22WX9012", "Truck", 17.5, "Belagavi Sugar Translines", "2023-10-25", "Available"),
    ("KA19YZ3456", "Trailer", 29.0, "Dakshina Kannada Logistics", "2023-08-30", "Available"),
    ("KA01AA7890", "Truck", 15.5, "Peenya Industrial Freight", "2024-01-28", "Available"),
    ("KA09BB1234", "Mini Truck", 4.2, "Nanjangud Fast Movers", "2024-02-17", "Available"),
    ("KA20CC5678", "Pickup", 2.5, "Kundapura Goods Service", "2024-03-10", "Available"),
    ("KA14DD9012", "Truck", 19.0, "Bhadravathi Steel Transport", "2023-11-14", "Available"),
    ("KA13EE3456", "Trailer", 31.0, "Western Ghats Haulers", "2023-07-15", "Available"),
    ("KA25FF7890", "Truck", 13.0, "Hubballi Commercial Trans", "2024-04-18", "Available"),
    ("KA22GG1234", "Mini Truck", 3.6, "Gokak Falls Freight", "2024-05-08", "Available"),
    ("KA19HH5678", "Pickup", 1.9, "Mangalore Tile Transporters", "2024-02-28", "Available"),
    ("KA01II9012", "Trailer", 34.0, "Outer Ring Road Logistics", "2023-09-12", "Available")
]

with open(os.path.join(datasets_dir, 'vehicles.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['vehicle_number', 'vehicle_type', 'capacity', 'owner_name', 'registration_date', 'availability_status'])
    w.writerows(vehicles)

# 2. drivers.csv (35 records >= 30)
drivers = [
    ("Raghavendra Rao", "9845011223", "KA1920150001001", "2028-05-20", "Available"),
    ("Manjunath Shetty", "9845022334", "KA2020160002002", "2029-03-15", "Available"),
    ("Santhosh Kumar", "9845033445", "KA0120140003003", "2027-11-10", "Available"),
    ("Praveen Poojary", "9845044556", "KA1920170004004", "2030-01-25", "Available"),
    ("Ganesh Acharya", "9845055667", "KA2020180005005", "2028-08-14", "Available"),
    ("Shivaraj Patil", "9845066778", "KA2520150006006", "2027-09-30", "Available"),
    ("Basavaraj Kulkarni", "9845077889", "KA2220160007007", "2029-06-18", "Available"),
    ("Dinesh Hegde", "9845088990", "KA1420170008008", "2028-12-05", "Available"),
    ("Chetan Gowda", "9845099001", "KA1320180009009", "2030-04-12", "Available"),
    ("Ravi Shankar", "9448011223", "KA0920150010010", "2027-07-22", "Available"),
    ("Anil Deshmukh", "9448022334", "KA2220160011011", "2029-10-08", "Available"),
    ("Sunil Nayak", "9448033445", "KA1920170012012", "2028-04-19", "Available"),
    ("Kiran Alva", "9448044556", "KA2020180013013", "2031-02-14", "Available"),
    ("Venkatesh Murthy", "9448055667", "KA0120140014014", "2027-08-01", "Available"),
    ("Naveen Dsouza", "9448066778", "KA1920160015015", "2028-11-28", "Available"),
    ("Prashanth Kulal", "9448077889", "KA2020170016016", "2029-05-17", "Available"),
    ("Suresh Belagavi", "9448088990", "KA2220180017017", "2030-09-23", "Available"),
    ("Yogesh Hubballi", "9448099001", "KA2520150018018", "2027-12-11", "Available"),
    ("Lokesh Hassan", "9741011223", "KA1320160019019", "2028-06-30", "Available"),
    ("Harish Shivamogga", "9741022334", "KA1420170020020", "2029-01-15", "Available"),
    ("Gururaj Bhat", "9741033445", "KA2020180021021", "2030-07-07", "Available"),
    ("Ashok Reddy", "9741044556", "KA0120150022022", "2028-03-25", "Available"),
    ("Mallikarjun Swamy", "9741055667", "KA2520160023023", "2027-10-18", "Available"),
    ("Deepak Mallya", "9741066778", "KA1920170024024", "2029-12-03", "Available"),
    ("Nagaraj Karkera", "9741077889", "KA2020180025025", "2031-05-09", "Available"),
    ("Vijay Kumar", "9741088990", "KA0920150026026", "2028-02-14", "Available"),
    ("Mahesh Shinde", "9741099001", "KA2220160027027", "2029-08-27", "Available"),
    ("Rajendra Prasad", "9632011223", "KA1420170028028", "2030-03-10", "Available"),
    ("Chandrashekar H", "9632022334", "KA1320180029029", "2027-11-29", "Available"),
    ("Sridhar Bangalore", "9632033445", "KA0120150030030", "2028-09-14", "Available"),
    ("Subhash Chandra", "9632044556", "KA2520160031031", "2029-04-20", "Available"),
    ("Umesh Kundapur", "9632055667", "KA2020170032032", "2030-10-16", "Available"),
    ("Mohan Mangalore", "9632066778", "KA1920180033033", "2028-01-30", "Available"),
    ("Anand Belagavi", "9632077889", "KA2220150034034", "2027-06-15", "Available"),
    ("Shankar Mysore", "9632088990", "KA0920160035035", "2029-11-05", "Available")
]

with open(os.path.join(datasets_dir, 'drivers.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['driver_name', 'phone_number', 'licence_number', 'licence_expiry_date', 'availability_status'])
    w.writerows(drivers)

# 3. loads.csv (55 records >= 50)
loads = [
    ("Karnataka Cement Corp", "9880011223", "Cement", "Mangaluru", "Bengaluru", 15.0, "Truck", "2026-10-01", 32000.0, "Posted"),
    ("Peenya Electronics Ltd", "9880022334", "Electronics", "Bengaluru", "Mysuru", 3.0, "Mini Truck", "2026-10-02", 12000.0, "Posted"),
    ("Bhadravathi Steel Works", "9880033445", "Steel", "Shivamogga", "Hubballi", 25.0, "Trailer", "2026-10-03", 45000.0, "Posted"),
    ("Kudla Wooden Furniture", "9880044556", "Furniture", "Mangaluru", "Udupi", 1.8, "Pickup", "2026-10-01", 6500.0, "Posted"),
    ("Mysuru Silk & Textiles", "9880055667", "Textiles", "Mysuru", "Bengaluru", 4.0, "Mini Truck", "2026-10-04", 14000.0, "Posted"),
    ("Hassan Agro Produce", "9880066778", "Food Grains", "Hassan", "Mangaluru", 14.0, "Truck", "2026-10-02", 24000.0, "Posted"),
    ("Belagavi Foundries", "9880077889", "Steel", "Belagavi", "Hubballi", 18.0, "Truck", "2026-10-05", 26000.0, "Posted"),
    ("Hubballi Cotton Mills", "9880088990", "Textiles", "Hubballi", "Bengaluru", 20.0, "Trailer", "2026-10-03", 38000.0, "Posted"),
    ("Udupi Food Spices", "9880099001", "Food Grains", "Udupi", "Shivamogga", 3.5, "Mini Truck", "2026-10-06", 11000.0, "Posted"),
    ("Coastal Tiles & Ceramics", "9148011223", "Cement", "Mangaluru", "Hassan", 12.0, "Truck", "2026-10-04", 21000.0, "Posted"),
    ("Bengaluru Office Decors", "9148022334", "Furniture", "Bengaluru", "Belagavi", 8.0, "Truck", "2026-10-07", 29000.0, "Posted"),
    ("Dharwad Transformers", "9148033445", "Electronics", "Hubballi", "Mangaluru", 16.0, "Truck", "2026-10-02", 33000.0, "Posted"),
    ("Shivamogga Iron Ores", "9148044556", "Steel", "Shivamogga", "Bengaluru", 30.0, "Trailer", "2026-10-05", 52000.0, "Posted"),
    ("Belagavi Sugar Refineries", "9148055667", "Food Grains", "Belagavi", "Mangaluru", 22.0, "Truck", "2026-10-03", 36000.0, "Posted"),
    ("Mysuru Timber Yards", "9148066778", "Furniture", "Mysuru", "Hassan", 2.0, "Pickup", "2026-10-08", 7500.0, "Posted"),
    ("Udupi Solar Systems", "9148077889", "Electronics", "Udupi", "Bengaluru", 5.0, "Mini Truck", "2026-10-04", 17000.0, "Posted"),
    ("Mangaluru Fish Feeds", "9148088990", "Food Grains", "Mangaluru", "Mysuru", 10.0, "Truck", "2026-10-06", 22000.0, "Posted"),
    ("Hassan Granites Ltd", "9148099001", "Cement", "Hassan", "Bengaluru", 28.0, "Trailer", "2026-10-07", 44000.0, "Posted"),
    ("Bengaluru Garment Exports", "9900011223", "Textiles", "Bengaluru", "Hubballi", 12.0, "Truck", "2026-10-02", 28000.0, "Posted"),
    ("Belagavi Heavy Castings", "9900022334", "Steel", "Belagavi", "Shivamogga", 14.5, "Truck", "2026-10-05", 27000.0, "Posted"),
    ("Shivamogga Paper Mills", "9900033445", "Textiles", "Shivamogga", "Mangaluru", 9.0, "Truck", "2026-10-03", 19000.0, "Posted"),
    ("Hubballi Seed Supplies", "9900044556", "Food Grains", "Hubballi", "Belagavi", 3.0, "Pickup", "2026-10-09", 8000.0, "Posted"),
    ("Mangaluru Refinery Pipes", "9900055667", "Steel", "Mangaluru", "Hubballi", 26.0, "Trailer", "2026-10-04", 48000.0, "Posted"),
    ("Bengaluru Computer Hardware", "9900066778", "Electronics", "Bengaluru", "Mangaluru", 2.5, "Pickup", "2026-10-01", 10500.0, "Posted"),
    ("Mysuru Sandal Artifacts", "9900077889", "Furniture", "Mysuru", "Udupi", 3.8, "Mini Truck", "2026-10-06", 13500.0, "Posted"),
    ("Udupi Coastal Masonry", "9900088990", "Cement", "Udupi", "Belagavi", 15.0, "Truck", "2026-10-08", 31000.0, "Posted"),
    ("Hassan Coffee Planters", "9900099001", "Food Grains", "Hassan", "Mysuru", 7.5, "Truck", "2026-10-02", 15000.0, "Posted"),
    ("Belagavi Aluminum Extrusions", "9844011223", "Steel", "Belagavi", "Bengaluru", 19.5, "Truck", "2026-10-05", 39000.0, "Posted"),
    ("Hubballi Railway Spares", "9844022334", "Steel", "Hubballi", "Mysuru", 22.0, "Trailer", "2026-10-07", 41000.0, "Posted"),
    ("Shivamogga Areca Merchants", "9844033445", "Food Grains", "Shivamogga", "Udupi", 4.2, "Mini Truck", "2026-10-03", 12500.0, "Posted"),
    ("Mangaluru Port Fertilizer", "9844044556", "Chemicals", "Mangaluru", "Belagavi", 16.0, "Truck", "2026-10-06", 34000.0, "Posted"),
    ("Bengaluru Automotive Assemblies", "9844055667", "Machinery", "Bengaluru", "Shivamogga", 11.0, "Truck", "2026-10-04", 25000.0, "Posted"),
    ("Mysuru Printing Inks", "9844066778", "Chemicals", "Mysuru", "Hubballi", 3.0, "Pickup", "2026-10-08", 11500.0, "Posted"),
    ("Udupi Marine Exports", "9844077889", "Food Grains", "Udupi", "Hassan", 6.0, "Truck", "2026-10-02", 16000.0, "Posted"),
    ("Hassan Coconut Traders", "9844088990", "Food Grains", "Hassan", "Hubballi", 13.0, "Truck", "2026-10-05", 23000.0, "Posted"),
    ("Belagavi Precision Pumps", "9844099001", "Machinery", "Belagavi", "Mysuru", 8.5, "Truck", "2026-10-07", 26000.0, "Posted"),
    ("Hubballi Electricals", "9740011223", "Electronics", "Hubballi", "Hassan", 2.2, "Pickup", "2026-10-03", 9500.0, "Posted"),
    ("Shivamogga Timber Crafts", "9740022334", "Furniture", "Shivamogga", "Belagavi", 5.5, "Mini Truck", "2026-10-09", 16500.0, "Posted"),
    ("Mangaluru Bitumen Logistics", "9740033445", "Chemicals", "Mangaluru", "Bengaluru", 24.0, "Trailer", "2026-10-04", 46000.0, "Posted"),
    ("Bengaluru Server Racks", "9740044556", "Electronics", "Bengaluru", "Udupi", 4.0, "Mini Truck", "2026-10-02", 15500.0, "Posted"),
    ("Mysuru Ayurvedic Formulations", "9740055667", "Chemicals", "Mysuru", "Mangaluru", 2.8, "Pickup", "2026-10-06", 11000.0, "Posted"),
    ("Udupi Temple Brasswares", "9740066778", "Machinery", "Udupi", "Mysuru", 3.2, "Mini Truck", "2026-10-05", 13000.0, "Posted"),
    ("Hassan Potato Chips Industry", "9740077889", "Food Grains", "Hassan", "Shivamogga", 7.0, "Truck", "2026-10-07", 17500.0, "Posted"),
    ("Belagavi Yarn Mills", "9740088990", "Textiles", "Belagavi", "Udupi", 10.5, "Truck", "2026-10-03", 24500.0, "Posted"),
    ("Hubballi Plastic Molders", "9740099001", "Furniture", "Hubballi", "Shivamogga", 6.5, "Truck", "2026-10-08", 18000.0, "Posted"),
    ("Shivamogga Ayurvedic Herbs", "9631011223", "Food Grains", "Shivamogga", "Hassan", 2.5, "Pickup", "2026-10-04", 8500.0, "Posted"),
    ("Mangaluru Granite Cutters", "9631022334", "Cement", "Mangaluru", "Shivamogga", 17.0, "Truck", "2026-10-02", 27000.0, "Posted"),
    ("Bengaluru Aerospace Rivets", "9631033445", "Machinery", "Bengaluru", "Belagavi", 3.6, "Mini Truck", "2026-10-06", 16000.0, "Posted"),
    ("Mysuru Silk Weavers Guild", "9631044556", "Textiles", "Mysuru", "Belagavi", 5.0, "Mini Truck", "2026-10-05", 19500.0, "Posted"),
    ("Udupi Power Cables", "9631055667", "Electronics", "Udupi", "Hubballi", 8.0, "Truck", "2026-10-07", 21500.0, "Posted"),
    ("Hassan Cardamom Exporters", "9631066778", "Food Grains", "Hassan", "Belagavi", 4.5, "Mini Truck", "2026-10-03", 15000.0, "Posted"),
    ("Belagavi Heavy Gears", "9631077889", "Machinery", "Belagavi", "Hassan", 15.0, "Truck", "2026-10-08", 29000.0, "Posted"),
    ("Hubballi Agro Tractors", "9631088990", "Machinery", "Hubballi", "Mangaluru", 20.0, "Trailer", "2026-10-04", 42000.0, "Posted"),
    ("Shivamogga Sand Mining", "9631099001", "Cement", "Shivamogga", "Mysuru", 28.0, "Trailer", "2026-10-06", 47000.0, "Posted"),
    ("Mangaluru Cashew Processors", "9631000112", "Food Grains", "Mangaluru", "Bengaluru", 11.5, "Truck", "2026-10-05", 26000.0, "Posted")
]

with open(os.path.join(datasets_dir, 'loads.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['customer_name', 'customer_phone', 'material_type', 'pickup_location', 'destination', 'load_weight', 'required_vehicle_type', 'pickup_date', 'offered_price', 'load_status'])
    w.writerows(loads)

# 4. vehicle_registration_test_data.csv
# Columns: test_case_id, test_scenario, vehicle_number, vehicle_type, capacity, owner_name, registration_date, availability_status, expected_result, expected_message, test_type, priority
v_test_data = [
    ("TC_VR_01", "Valid vehicle registration - Truck", "KA19XY1111", "Truck", "15.0", "Kudla Express Lines", "2026-09-01", "Available", "Success", "Vehicle KA19XY1111 successfully registered!", "Positive", "High"),
    ("TC_VR_02", "Valid vehicle registration - Mini Truck", "KA01MN2222", "Mini Truck", "3.5", "Metro Logistics", "2026-09-05", "Available", "Success", "Vehicle KA01MN2222 successfully registered!", "Positive", "High"),
    ("TC_VR_03", "Empty vehicle number", "", "Truck", "10.0", "Anand Roadways", "2026-09-10", "Available", "Failure", "Vehicle number is required.", "Negative", "High"),
    ("TC_VR_04", "Invalid vehicle number format - Missing digits", "KA19AB", "Truck", "12.0", "Coastal Haulage", "2026-09-12", "Available", "Failure", "Invalid Indian vehicle registration number format", "Negative", "High"),
    ("TC_VR_05", "Invalid vehicle number format - Special characters", "KA-19-AB-1234$", "Truck", "12.0", "Coastal Haulage", "2026-09-12", "Available", "Failure", "Invalid Indian vehicle registration number format", "Negative", "Medium"),
    ("TC_VR_06", "Duplicate vehicle number", "KA19AB1234", "Truck", "16.0", "Duplicate Owner", "2026-09-15", "Available", "Failure", "already registered", "Negative", "High"),
    ("TC_VR_07", "Zero capacity boundary check", "KA20CD3333", "Trailer", "0", "Udupi Freight", "2026-09-15", "Available", "Failure", "Capacity must be greater than zero tonnes.", "Boundary", "High"),
    ("TC_VR_08", "Negative capacity boundary check", "KA20EF4444", "Trailer", "-5.0", "Udupi Freight", "2026-09-15", "Available", "Failure", "Capacity must be greater than zero tonnes.", "Boundary", "High"),
    ("TC_VR_09", "Smallest valid positive capacity boundary check", "KA14GH5555", "Pickup", "0.1", "Sahyadri Parcel", "2026-09-18", "Available", "Success", "Vehicle KA14GH5555 successfully registered!", "Boundary", "Medium"),
    ("TC_VR_10", "Empty owner name", "KA13IJ6666", "Mini Truck", "4.0", "", "2026-09-20", "Available", "Failure", "Owner name is required.", "Negative", "Medium"),
    ("TC_VR_11", "Valid vehicle registration - Trailer with high capacity", "KA25KL7777", "Trailer", "40.0", "North Karnataka Trans", "2026-09-22", "Available", "Success", "Vehicle KA25KL7777 successfully registered!", "Positive", "Medium")
]

with open(os.path.join(datasets_dir, 'vehicle_registration_test_data.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['test_case_id', 'test_scenario', 'vehicle_number', 'vehicle_type', 'capacity', 'owner_name', 'registration_date', 'availability_status', 'expected_result', 'expected_message', 'test_type', 'priority'])
    w.writerows(v_test_data)

# 5. driver_registration_test_data.csv
# Columns: test_case_id, test_scenario, driver_name, phone_number, licence_number, licence_expiry_date, availability_status, expected_result, expected_message, test_type, priority
d_test_data = [
    ("TC_DR_01", "Valid driver registration with future licence expiry", "Ramesh Poojary", "9886012345", "KA1920210009999", "2029-12-31", "Available", "Success", "Driver Ramesh Poojary successfully registered!", "Positive", "High"),
    ("TC_DR_02", "Empty driver name", "", "9886023456", "KA1920210008888", "2029-12-31", "Available", "Failure", "Driver name is required.", "Negative", "High"),
    ("TC_DR_03", "Invalid phone number - Less than 10 digits (9 digits)", "Ravi Kumar", "988601234", "KA1920210007777", "2029-12-31", "Available", "Failure", "Phone number must contain exactly 10 digits.", "Negative", "High"),
    ("TC_DR_04", "Invalid phone number - More than 10 digits (11 digits)", "Sunil Gowda", "98860123456", "KA1920210006666", "2029-12-31", "Available", "Failure", "Phone number must contain exactly 10 digits.", "Negative", "High"),
    ("TC_DR_05", "Duplicate phone number registration", "Kiran Hegde", "9845011223", "KA1920210005555", "2029-12-31", "Available", "Failure", "Phone number 9845011223 is already registered", "Negative", "High"),
    ("TC_DR_06", "Duplicate licence number registration", "Mahesh Alva", "9886034567", "KA1920150001001", "2029-12-31", "Available", "Failure", "already registered", "Negative", "High"),
    ("TC_DR_07", "Expired licence date boundary check - Past date", "Gopal Shetty", "9886045678", "KA1920210004444", "2022-01-01", "Available", "Failure", "Licence expiry date must be a future date.", "Boundary", "High"),
    ("TC_DR_08", "Expired licence date boundary check - Today date", "Pradeep Rai", "9886056789", "KA1920210003333", "2026-09-19", "Available", "Failure", "Licence expiry date must be a future date.", "Boundary", "High"),
    ("TC_DR_09", "Valid boundary future date - Tomorrow date", "Vinod Nayak", "9886067890", "KA1920210002222", "2026-09-20", "Available", "Success", "Driver Vinod Nayak successfully registered!", "Boundary", "Medium"),
    ("TC_DR_10", "Empty licence number", "Arun Kumar", "9886078901", "", "2029-12-31", "Available", "Failure", "Driving licence number is required.", "Negative", "High")
]

with open(os.path.join(datasets_dir, 'driver_registration_test_data.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['test_case_id', 'test_scenario', 'driver_name', 'phone_number', 'licence_number', 'licence_expiry_date', 'availability_status', 'expected_result', 'expected_message', 'test_type', 'priority'])
    w.writerows(d_test_data)

# 6. load_posting_test_data.csv
# Columns: test_case_id, test_scenario, customer_name, customer_phone, material_type, pickup_location, destination, load_weight, required_vehicle_type, pickup_date, offered_price, expected_result, expected_message, test_type, priority
l_test_data = [
    ("TC_LP_01", "Valid load posting with positive weight and price", "Karnataka Steel Corp", "9845112233", "Steel", "Mangaluru", "Bengaluru", "14.5", "Truck", "2026-10-15", "35000", "Success", "successfully posted!", "Positive", "High"),
    ("TC_LP_02", "Empty customer name", "", "9845112233", "Steel", "Mangaluru", "Bengaluru", "14.5", "Truck", "2026-10-15", "35000", "Failure", "Customer name is required.", "Negative", "High"),
    ("TC_LP_03", "Invalid customer phone - 8 digits", "Anand Rao", "98451122", "Furniture", "Udupi", "Mysuru", "2.5", "Pickup", "2026-10-15", "8000", "Failure", "Customer phone number must contain exactly 10 digits.", "Negative", "High"),
    ("TC_LP_04", "Empty pickup location", "Canara Merchants", "9845112233", "Cement", "", "Bengaluru", "12.0", "Truck", "2026-10-15", "25000", "Failure", "Pickup location is required.", "Negative", "High"),
    ("TC_LP_05", "Same pickup and destination location", "Coastal Traders", "9845112233", "Cement", "Mangaluru", "Mangaluru", "12.0", "Truck", "2026-10-15", "25000", "Failure", "Pickup location and destination cannot be the same.", "Negative", "High"),
    ("TC_LP_06", "Same pickup and destination with different casing and spaces", "Coastal Traders", "9845112233", "Cement", "  bengaluru ", "Bengaluru  ", "12.0", "Truck", "2026-10-15", "25000", "Failure", "Pickup location and destination cannot be the same.", "Boundary", "High"),
    ("TC_LP_07", "Zero load weight boundary check", "Malnad Timber", "9845112233", "Furniture", "Shivamogga", "Hubballi", "0", "Mini Truck", "2026-10-15", "12000", "Failure", "Load weight must be a positive number greater than zero.", "Boundary", "High"),
    ("TC_LP_08", "Negative load weight boundary check", "Malnad Timber", "9845112233", "Furniture", "Shivamogga", "Hubballi", "-3.5", "Mini Truck", "2026-10-15", "12000", "Failure", "Load weight must be a positive number greater than zero.", "Boundary", "High"),
    ("TC_LP_09", "Zero offered price boundary check", "Hassan Agro Foods", "9845112233", "Food Grains", "Hassan", "Belagavi", "8.0", "Truck", "2026-10-15", "0", "Failure", "Offered price must be greater than zero.", "Boundary", "High"),
    ("TC_LP_10", "Negative offered price boundary check", "Hassan Agro Foods", "9845112233", "Food Grains", "Hassan", "Belagavi", "8.0", "Truck", "2026-10-15", "-1000", "Failure", "Offered price must be greater than zero.", "Boundary", "High"),
    ("TC_LP_11", "Past pickup date boundary check", "Belagavi Traders", "9845112233", "Textiles", "Belagavi", "Bengaluru", "5.0", "Mini Truck", "2025-01-01", "18000", "Failure", "Pickup date cannot be in the past.", "Boundary", "High"),
    ("TC_LP_12", "Valid boundary - Small weight and today pickup date", "Udupi Spices", "9845112233", "Food Grains", "Udupi", "Mangaluru", "0.5", "Pickup", "2026-09-19", "4500", "Success", "successfully posted!", "Boundary", "Medium")
]

with open(os.path.join(datasets_dir, 'load_posting_test_data.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['test_case_id', 'test_scenario', 'customer_name', 'customer_phone', 'material_type', 'pickup_location', 'destination', 'load_weight', 'required_vehicle_type', 'pickup_date', 'offered_price', 'expected_result', 'expected_message', 'test_type', 'priority'])
    w.writerows(l_test_data)

# 7. load_search_test_data.csv
# Columns: test_case_id, test_scenario, pickup_location, destination, material_type, required_vehicle_type, min_weight, max_weight, load_status, expected_result, expected_message, test_type, priority
s_test_data = [
    ("TC_LS_01", "Search by pickup location - Mangaluru", "Mangaluru", "", "", "", "", "", "", "Results_Found", "Mangaluru", "Positive", "High"),
    ("TC_LS_02", "Search by destination - Bengaluru", "", "Bengaluru", "", "", "", "", "", "Results_Found", "Bengaluru", "Positive", "High"),
    ("TC_LS_03", "Search by material type - Cement", "", "", "Cement", "", "", "", "", "Results_Found", "Cement", "Positive", "High"),
    ("TC_LS_04", "Search by required vehicle type - Trailer", "", "", "", "Trailer", "", "", "", "Results_Found", "Trailer", "Positive", "Medium"),
    ("TC_LS_05", "Search by weight range - 10 to 20 tonnes", "", "", "", "", "10.0", "20.0", "", "Results_Found", "10 to 20", "Boundary", "High"),
    ("TC_LS_06", "Search with no matching records - Non-existent location", "KashmirValleys123", "", "", "", "", "", "", "No_Results", "No matching loads found", "Negative", "High"),
    ("TC_LS_07", "Search with impossible weight filter - Min 100 Tonnes", "", "", "", "", "100.0", "200.0", "", "No_Results", "No matching loads found", "Boundary", "Medium"),
    ("TC_LS_08", "Search by status - Posted", "", "", "", "", "", "", "Posted", "Results_Found", "Posted", "Positive", "Medium")
]

with open(os.path.join(datasets_dir, 'load_search_test_data.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['test_case_id', 'test_scenario', 'pickup_location', 'destination', 'material_type', 'required_vehicle_type', 'min_weight', 'max_weight', 'load_status', 'expected_result', 'expected_message', 'test_type', 'priority'])
    w.writerows(s_test_data)

# 8. booking_test_data.csv
# Columns: test_case_id, test_scenario, load_weight, vehicle_capacity, vehicle_status, driver_status, expected_result, expected_message, test_type, priority
b_test_data = [
    ("TC_BK_01", "Valid assignment - Vehicle capacity greater than load weight", 10.0, 16.0, "Available", "Available", "Success", "successfully created and confirmed", "Positive", "High"),
    ("TC_BK_02", "Boundary assignment - Vehicle capacity exactly equal to load weight", 15.0, 15.0, "Available", "Available", "Success", "successfully created and confirmed", "Boundary", "High"),
    ("TC_BK_03", "Invalid assignment - Vehicle capacity strictly less than load weight", 20.0, 12.0, "Available", "Available", "Failure", "Insufficient vehicle capacity", "Negative", "High"),
    ("TC_BK_04", "Invalid assignment - Selected vehicle is currently Unavailable", 10.0, 16.0, "Unavailable", "Available", "Failure", "currently Unavailable", "Negative", "High"),
    ("TC_BK_05", "Invalid assignment - Selected driver is currently Unavailable", 10.0, 16.0, "Available", "Unavailable", "Failure", "currently Unavailable", "Negative", "High"),
    ("TC_BK_06", "Booking cancellation - Restores vehicle and driver availability", 8.0, 15.0, "Assigned", "Assigned", "Success", "has been cancelled. Vehicle and Driver are now Available", "Positive", "High")
]

with open(os.path.join(datasets_dir, 'booking_test_data.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['test_case_id', 'test_scenario', 'load_weight', 'vehicle_capacity', 'vehicle_status', 'driver_status', 'expected_result', 'expected_message', 'test_type', 'priority'])
    w.writerows(b_test_data)

# 9. manual_test_cases.csv (35 manual test cases >= 30)
# Columns: Test Case ID, Module, Test Scenario, Preconditions, Test Steps, Test Data, Expected Result, Actual Result, Status, Priority
manual_test_cases = [
    ("TC_MAN_01", "Vehicle Registration", "Verify successful registration with valid inputs", "User is on Vehicles page", "1. Enter valid vehicle number\n2. Select vehicle type\n3. Enter capacity > 0\n4. Enter owner name\n5. Enter registration date\n6. Click Register Vehicle", "KA19AB1234, Truck, 16.0T, Ramesh Transport, 2024-01-15", "Success alert displayed; record added to table", "", "", "High"),
    ("TC_MAN_02", "Vehicle Registration", "Verify validation on empty vehicle number", "User is on Vehicles page", "1. Leave vehicle number empty\n2. Fill remaining fields\n3. Click Register", "Empty vehicle number", "Validation error: 'Vehicle number is required.'", "", "", "High"),
    ("TC_MAN_03", "Vehicle Registration", "Verify validation on non-Indian format vehicle number", "User is on Vehicles page", "1. Enter invalid string 'XYZ-123'\n2. Click Register", "XYZ-123", "Error: 'Invalid Indian vehicle registration number format'", "", "", "High"),
    ("TC_MAN_04", "Vehicle Registration", "Verify rejection of duplicate vehicle number", "Vehicle KA19AB1234 already registered", "1. Enter existing vehicle number 'KA19AB1234'\n2. Submit form", "KA19AB1234", "Error: 'Vehicle number KA19AB1234 is already registered.'", "", "", "High"),
    ("TC_MAN_05", "Vehicle Registration", "Boundary: Zero capacity validation", "User is on Vehicles page", "1. Enter capacity '0'\n2. Submit form", "Capacity = 0", "Error: 'Capacity must be greater than zero tonnes.'", "", "", "High"),
    ("TC_MAN_06", "Vehicle Registration", "Boundary: Negative capacity validation", "User is on Vehicles page", "1. Enter capacity '-5.5'\n2. Submit form", "Capacity = -5.5", "Error: 'Capacity must be greater than zero tonnes.'", "", "", "High"),
    ("TC_MAN_07", "Vehicle Registration", "Boundary: Minimum positive capacity (0.1T)", "User is on Vehicles page", "1. Enter capacity '0.1'\n2. Submit form", "Capacity = 0.1", "Vehicle registered successfully", "", "", "Medium"),
    ("TC_MAN_08", "Vehicle Registration", "Verify edit vehicle details", "Vehicle exists in database", "1. Click Edit icon on vehicle row\n2. Modify owner name\n3. Click Save Changes", "New owner name", "Vehicle details updated successfully in list", "", "", "Medium"),
    ("TC_MAN_09", "Vehicle Registration", "Verify vehicle deletion with no active booking", "Vehicle has no active booking", "1. Click Delete button\n2. Confirm alert dialog", "Vehicle ID", "Vehicle removed from table", "", "", "Medium"),
    ("TC_MAN_10", "Driver Registration", "Verify driver registration with valid details", "User is on Drivers page", "1. Enter driver name\n2. Enter 10-digit phone\n3. Enter unique licence\n4. Select future expiry date\n5. Click Register Driver", "Suresh Rao, 9845011223, KA1920150001001, 2029-05-20", "Driver registered successfully and shown in table", "", "", "High"),
    ("TC_MAN_11", "Driver Registration", "Verify phone number with less than 10 digits", "User is on Drivers page", "1. Enter 9-digit phone number\n2. Click Register", "984501122", "Error: 'Phone number must contain exactly 10 digits.'", "", "", "High"),
    ("TC_MAN_12", "Driver Registration", "Verify phone number with more than 10 digits", "User is on Drivers page", "1. Enter 11-digit phone number\n2. Click Register", "98450112233", "Error: 'Phone number must contain exactly 10 digits.'", "", "", "High"),
    ("TC_MAN_13", "Driver Registration", "Verify duplicate driver phone number rejection", "Driver with phone 9845011223 exists", "1. Enter phone 9845011223\n2. Fill valid other details\n3. Click Register", "Phone 9845011223", "Error: 'Phone number is already registered'", "", "", "High"),
    ("TC_MAN_14", "Driver Registration", "Verify duplicate licence number rejection", "Driver with DL KA1920150001001 exists", "1. Enter DL KA1920150001001\n2. Submit", "DL KA1920150001001", "Error: 'Licence number is already registered'", "", "", "High"),
    ("TC_MAN_15", "Driver Registration", "Boundary: Past licence expiry date rejection", "User is on Drivers page", "1. Enter expiry date '2023-01-01'\n2. Submit", "Expiry: 2023-01-01", "Error: 'Licence expiry date must be a future date.'", "", "", "High"),
    ("TC_MAN_16", "Driver Registration", "Boundary: Today date as expiry date rejection", "User is on Drivers page", "1. Enter current date\n2. Submit", "Expiry: Today", "Error: 'Licence expiry date must be a future date.'", "", "", "Medium"),
    ("TC_MAN_17", "Load Posting", "Verify posting load with valid inputs", "User is on Loads page", "1. Enter customer name\n2. Enter 10-digit phone\n3. Select material\n4. Enter pickup & destination\n5. Enter weight > 0\n6. Select vehicle\n7. Enter future date & price\n8. Click Post Load", "Cement, Mangaluru to Bengaluru, 15T, Price 32000", "Load posted successfully and status displayed as Posted", "", "", "High"),
    ("TC_MAN_18", "Load Posting", "Verify validation when pickup equals destination", "User is on Loads page", "1. Enter Pickup = 'Mangaluru'\n2. Enter Destination = 'Mangaluru'\n3. Submit", "Pickup=Mangaluru, Dest=Mangaluru", "Error: 'Pickup location and destination cannot be the same.'", "", "", "High"),
    ("TC_MAN_19", "Load Posting", "Boundary: Same pickup and destination case-insensitive", "User is on Loads page", "1. Enter Pickup = 'bengaluru'\n2. Enter Destination = 'BENGALURU'\n3. Submit", "Pickup=bengaluru, Dest=BENGALURU", "Error: 'Pickup location and destination cannot be the same.'", "", "", "High"),
    ("TC_MAN_20", "Load Posting", "Boundary: Zero and negative load weight", "User is on Loads page", "1. Enter weight '0' or '-5'\n2. Submit", "Weight <= 0", "Error: 'Load weight must be a positive number greater than zero.'", "", "", "High"),
    ("TC_MAN_21", "Load Posting", "Boundary: Past pickup date rejection", "User is on Loads page", "1. Enter pickup date '2025-01-01'\n2. Submit", "Date: 2025-01-01", "Error: 'Pickup date cannot be in the past.'", "", "", "High"),
    ("TC_MAN_22", "Load Posting", "Boundary: Zero or negative offered price rejection", "User is on Loads page", "1. Enter price <= 0\n2. Submit", "Price: 0 or -100", "Error: 'Offered price must be greater than zero.'", "", "", "High"),
    ("TC_MAN_23", "Load Search", "Verify search filter by pickup location", "Multiple loads exist", "1. Enter 'Mangaluru' in Pickup Location\n2. Click Search", "Pickup: Mangaluru", "Table displays only loads originating from Mangaluru", "", "", "High"),
    ("TC_MAN_24", "Load Search", "Verify search filter by weight range", "Loads of varying weights exist", "1. Enter Min Weight = 10, Max Weight = 20\n2. Click Search", "Weight: 10 - 20T", "Only loads with weight between 10T and 20T displayed", "", "", "Medium"),
    ("TC_MAN_25", "Load Search", "Verify 'No matching loads found' message", "User is on Search page", "1. Enter non-existent keyword in Pickup Location\n2. Click Search", "Pickup: NonExistentPlace999", "'No matching loads found' message container displayed", "", "", "High"),
    ("TC_MAN_26", "Vehicle & Driver Assignment", "Verify successful assignment when capacity >= weight", "Load (15T), Vehicle (16T Available), Driver (Available)", "1. Select Load #1\n2. Select Vehicle (16T)\n3. Select Driver\n4. Click Confirm Assignment", "Load 15T, Vehicle 16T", "Booking generated, redirected to Confirmation voucher", "", "", "High"),
    ("TC_MAN_27", "Vehicle & Driver Assignment", "Boundary: Vehicle capacity strictly equal to load weight", "Load (15T), Vehicle (15T Available), Driver (Available)", "1. Select Load (15T)\n2. Select Vehicle (15T)\n3. Select Driver\n4. Click Confirm Assignment", "Load 15T, Vehicle 15T", "Assignment successful and Confirmed", "", "", "High"),
    ("TC_MAN_28", "Vehicle & Driver Assignment", "Verify rejection when vehicle capacity < load weight", "Load (20T), Vehicle (12T Available), Driver (Available)", "1. Select Load (20T)\n2. Select Vehicle (12T)\n3. Submit assignment", "Load 20T, Vehicle 12T", "Error: 'Insufficient vehicle capacity: Vehicle capacity is less than load weight.'", "", "", "High"),
    ("TC_MAN_29", "Vehicle & Driver Assignment", "Verify vehicle and driver status update to Unavailable", "Successful assignment made", "1. Check Vehicles table\n2. Check Drivers table", "Assigned vehicle & driver", "Both statuses show 'Unavailable'", "", "", "High"),
    ("TC_MAN_30", "Vehicle & Driver Assignment", "Verify double-booking prevention of assigned vehicle", "Vehicle already assigned to active booking", "1. Try assigning same vehicle to another load", "Assigned Vehicle", "Unavailable in dropdown or rejected with error", "", "", "High"),
    ("TC_MAN_31", "Booking Confirmation", "Verify voucher details display accurately", "Booking has been confirmed", "1. Open Booking Confirmation voucher\n2. Inspect customer, load, vehicle, and driver fields", "Booking ID", "All details match database record exactly", "", "", "High"),
    ("TC_MAN_32", "Booking Cancellation", "Verify cancellation resets vehicle and driver status", "Active booking exists", "1. Click Cancel Booking button\n2. Confirm dialog", "Active Booking", "Booking status becomes 'Cancelled', vehicle & driver become 'Available'", "", "", "High"),
    ("TC_MAN_33", "Booking Registry", "Verify booking filter tabs (All, Confirmed, Cancelled)", "Both Confirmed and Cancelled bookings exist", "1. Click 'Confirmed' tab\n2. Click 'Cancelled' tab", "Filter tabs", "Table filters correctly according to selected status", "", "", "Medium"),
    ("TC_MAN_34", "Dataset Import", "Verify importing valid vehicles CSV", "vehicles.csv file available", "1. Go to Import Dataset page\n2. Select Vehicles\n3. Choose CSV\n4. Click Import", "vehicles.csv", "Success alert with imported and skipped counts", "", "", "High"),
    ("TC_MAN_35", "Dataset Import", "Verify error handling on invalid/corrupted CSV structure", "Invalid CSV with missing columns", "1. Upload CSV with missing columns\n2. Click Import", "Corrupted CSV", "Error alert: 'Missing required columns in CSV'", "", "", "High")
]

with open(os.path.join(project_dir, 'manual_test_cases.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Test Case ID', 'Module', 'Test Scenario', 'Preconditions', 'Test Steps', 'Test Data', 'Expected Result', 'Actual Result', 'Status', 'Priority'])
    w.writerows(manual_test_cases)

print("All 9 CSV datasets and manual test cases successfully generated!")
