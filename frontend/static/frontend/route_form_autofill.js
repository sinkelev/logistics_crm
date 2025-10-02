document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form[data-drivers-map]');
  if (!form) {
    return;
  }

  const routeNumberInput = document.getElementById('id_route_number');
  const dateStartInput = document.getElementById('id_date_start');
  const driverSelect = document.getElementById('id_driver');
  const vehicleSelect = document.getElementById('id_vehicle');

  if (!routeNumberInput || !dateStartInput || !driverSelect || !vehicleSelect) {
    return;
  }

  const driversMap = JSON.parse(form.dataset.driversMap);
  const vehiclesMap = JSON.parse(form.dataset.vehiclesMap);

  const updateRouteNumber = () => {
    if (routeNumberInput.dataset.manualEdit === 'true' && routeNumberInput.value.trim() !== '') {
        return;
    }

    const dateValue = dateStartInput.value;
    const driverId = driverSelect.value;
    const vehicleId = vehicleSelect.value;

    if (!dateValue || !driverId || !vehicleId) {
      return;
    }

    try {
      const date = new Date(dateValue);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = String(date.getFullYear()).slice(-2);
      const formattedDate = `${day}.${month}.${year}`;

      const driverLastName = driversMap[driverId] || '';
      const vehiclePlate = vehiclesMap[vehicleId] || '';

      if (driverLastName && vehiclePlate) {
        const newRouteNumber = `${formattedDate}-${driverLastName}-${vehiclePlate}`;
        routeNumberInput.value = newRouteNumber;
      }
    } catch (e) {
      console.error("Invalid date format", e);
    }
  };

  dateStartInput.addEventListener('change', updateRouteNumber);
  driverSelect.addEventListener('change', updateRouteNumber);
  vehicleSelect.addEventListener('change', updateRouteNumber);

  routeNumberInput.addEventListener('input', () => {
    routeNumberInput.dataset.manualEdit = 'true';
  });

  updateRouteNumber();
});