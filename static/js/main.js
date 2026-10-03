// Client-side JavaScript helpers for Transport Load Booking System
document.addEventListener('DOMContentLoaded', () => {
    // Auto-uppercase vehicle numbers
    const vehicleInputs = document.querySelectorAll('#vehicle_number, #edit_vehicle_number');
    vehicleInputs.forEach(input => {
        input.addEventListener('input', () => {
            input.value = input.value.toUpperCase();
        });
    });

    // Auto-uppercase licence numbers
    const licenceInputs = document.querySelectorAll('#driver_licence, #edit_driver_licence');
    licenceInputs.forEach(input => {
        input.addEventListener('input', () => {
            input.value = input.value.toUpperCase();
        });
    });

    // Enforce 10 digits numeric only on phone numbers
    const phoneInputs = document.querySelectorAll('#driver_phone, #edit_driver_phone, #customer_phone, #edit_customer_phone');
    phoneInputs.forEach(input => {
        input.addEventListener('input', () => {
            input.value = input.value.replace(/\D/g, '').slice(0, 10);
        });
    });
});
