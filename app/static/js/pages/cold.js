CF.state.coldTab = CF.state.coldTab || "status";

CF.renderCold = function renderCold() {
  const tab = CF.state.coldTab || "status";
  CF.$("#view-cold").innerHTML = `
    <div class="toolbar split-toolbar">
      <div class="segmented-control" role="group" aria-label="Secciones de frio">
        ${CF.coldTabButton("status", "Estado", tab)}
        ${CF.coldTabButton("locations", "Camaras", tab)}
        ${CF.coldTabButton("sensors", "Sensores", tab)}
        ${CF.coldTabButton("readings", "Lecturas", tab)}
      </div>
      ${tab === "locations" ? `<button class="secondary-btn toolbar-action" type="button" id="open-location">Nueva camara</button>` : ""}
      ${tab === "sensors" ? `<button class="secondary-btn toolbar-action" type="button" id="open-sensor">Nuevo sensor</button>` : ""}
    </div>
    ${CF.renderColdTab(tab)}
  `;

  CF.$$('[data-cold-tab]').forEach((button) => button.addEventListener("click", () => {
    CF.state.coldTab = button.dataset.coldTab;
    CF.renderCold();
  }));
  CF.bindColdTabActions(tab);
};

CF.coldTabButton = function coldTabButton(value, label, activeTab) {
  return `<button class="segment-btn ${activeTab === value ? "is-active" : ""}" type="button" data-cold-tab="${value}">${label}</button>`;
};

CF.renderColdTab = function renderColdTab(tab) {
  const renderers = {
    status: CF.renderColdStatus,
    locations: CF.renderColdLocations,
    sensors: CF.renderColdSensors,
    readings: CF.renderColdReadings,
  };
  return (renderers[tab] || CF.renderColdStatus)();
};

CF.bindColdTabActions = function bindColdTabActions(tab) {
  if (tab === "locations") {
    CF.$("#open-location").addEventListener("click", () => CF.openColdLocationModal());
    CF.$$('[data-edit-location]').forEach((button) => button.addEventListener("click", () => CF.openColdLocationModal(Number(button.dataset.editLocation))));
    CF.$$('[data-delete-location]').forEach((button) => button.addEventListener("click", () => {
      CF.confirmDelete("La camara o zona quedara inactiva para nuevos movimientos. Continuar?", `/cold-locations/${button.dataset.deleteLocation}`);
    }));
  }
  if (tab === "sensors") {
    CF.$("#open-sensor").addEventListener("click", () => CF.openSensorModal());
    CF.$$('[data-reading-sensor]').forEach((button) => button.addEventListener("click", () => CF.openReadingModal(Number(button.dataset.readingSensor))));
    CF.$$('[data-edit-sensor]').forEach((button) => button.addEventListener("click", () => CF.openSensorModal(Number(button.dataset.editSensor))));
    CF.$$('[data-delete-sensor]').forEach((button) => button.addEventListener("click", () => {
      CF.confirmDelete("El sensor quedara inactivo para nuevas lecturas. Continuar?", `/sensors/${button.dataset.deleteSensor}`);
    }));
  }
  if (tab === "readings") {
    CF.$("#open-reading").addEventListener("click", () => CF.openReadingModal());
  }
};

CF.latestReadingForSensor = function latestReadingForSensor(sensorId) {
  return CF.state.data.readings.find((reading) => Number(reading.device_id) === Number(sensorId));
};

CF.sensorOperationalStatus = function sensorOperationalStatus(sensor) {
  if (!sensor.is_active) return { value: "inactive", label: "Inactivo" };
  const reading = CF.latestReadingForSensor(sensor.id);
  if (!reading) return { value: "pending", label: "Sin lectura" };

  const location = CF.state.data.locations.find((item) => Number(item.id) === Number(sensor.cold_location_id));
  if (!location || !location.is_active) return { value: "inactive", label: "Zona inactiva" };

  const tempOut = reading.temperature !== null && reading.temperature !== undefined && (
    (location.min_temperature !== null && location.min_temperature !== undefined && reading.temperature < location.min_temperature)
    || (location.max_temperature !== null && location.max_temperature !== undefined && reading.temperature > location.max_temperature)
  );
  const humidityOut = reading.humidity !== null && reading.humidity !== undefined && (
    (location.min_humidity !== null && location.min_humidity !== undefined && reading.humidity < location.min_humidity)
    || (location.max_humidity !== null && location.max_humidity !== undefined && reading.humidity > location.max_humidity)
  );

  if (tempOut || humidityOut) return { value: "critical", label: "Fuera de rango" };
  return { value: "active", label: "OK" };
};

CF.renderColdStatus = function renderColdStatus() {
  const activeSensors = CF.activeItems(CF.state.data.sensors);
  const statuses = activeSensors.map(CF.sensorOperationalStatus);
  const outOfRange = statuses.filter((status) => status.value === "critical").length;
  const withoutReading = statuses.filter((status) => status.value === "pending").length;
  return `
    <div class="grid cols-3">
      ${CF.statCard("Sensores activos", activeSensors.length, "Dispositivos operativos")}
      ${CF.statCard("Fuera de rango", outOfRange, "Requieren atencion")}
      ${CF.statCard("Sin lectura", withoutReading, "Pendientes de registrar")}
    </div>
    <article class="panel" style="margin-top:14px">
      <div class="panel-head"><div><h2>Estado actual</h2><p>Ultima lectura por sensor y zona asignada.</p></div></div>
      ${CF.renderSensorStatusTable(activeSensors)}
    </article>
  `;
};

CF.renderColdLocations = function renderColdLocations() {
  return `
    <article class="panel">
      <div class="panel-head"><div><h2>Camaras y zonas</h2><p>Rangos esperados de operacion.</p></div></div>
      ${CF.table(["Zona", "Tipo", "Temp.", "Humedad", "Estado", "Acciones"], CF.state.data.locations.map((location) => [
        CF.escapeHtml(location.name),
        CF.escapeHtml(location.location_type),
        `${location.min_temperature ?? "-"} / ${location.max_temperature ?? "-"}`,
        `${location.min_humidity ?? "-"} / ${location.max_humidity ?? "-"}`,
        CF.statusPill(location.is_active ? "active" : "inactive", CF.statusLabel(location.is_active)),
        CF.actionButtons("location", location.id, location.is_active),
      ]))}
    </article>
  `;
};

CF.renderColdSensors = function renderColdSensors() {
  return `
    <article class="panel">
      <div class="panel-head"><div><h2>Sensores</h2><p>Un sensor pertenece a una sola camara o zona.</p></div></div>
      ${CF.renderSensorStatusTable(CF.state.data.sensors, true)}
    </article>
  `;
};

CF.renderColdReadings = function renderColdReadings() {
  return `
    <div class="toolbar split-toolbar">
      <button class="secondary-btn toolbar-action" type="button" id="open-reading">Registrar lectura</button>
    </div>
    <article class="panel">
      <div class="panel-head"><div><h2>Ultimas lecturas</h2><p>Historial reciente registrado por sensor.</p></div></div>
      ${CF.renderReadingsTable(CF.state.data.readings.slice(0, 50))}
    </article>
  `;
};

CF.renderSensorStatusTable = function renderSensorStatusTable(sensors, withActions = false) {
  return CF.table(["Sensor", "Zona", "Tipo", "Temp.", "Humedad", "Ultima lectura", "Estado", withActions ? "Acciones" : ""], sensors.map((sensor) => {
    const reading = CF.latestReadingForSensor(sensor.id);
    const status = CF.sensorOperationalStatus(sensor);
    return [
      CF.escapeHtml(sensor.name),
      CF.locationName(sensor.cold_location_id),
      CF.escapeHtml(sensor.sensor_type),
      reading?.temperature ?? "-",
      reading?.humidity ?? "-",
      reading ? CF.fmtDate(reading.recorded_at) : "-",
      CF.statusPill(status.value, status.label),
      withActions ? CF.sensorActionButtons(sensor) : "",
    ];
  }));
};

CF.sensorActionButtons = function sensorActionButtons(sensor) {
  return `
    <div class="table-actions">
      <button class="primary-btn compact-btn" data-reading-sensor="${sensor.id}" type="button">Lectura</button>
      <button class="secondary-btn compact-btn" data-edit-sensor="${sensor.id}" type="button">Editar</button>
      ${sensor.is_active ? `<button class="danger-btn compact-btn" data-delete-sensor="${sensor.id}" type="button">Borrar</button>` : ""}
    </div>
  `;
};

CF.renderReadingsTable = function renderReadingsTable(readings) {
  return CF.table(["Fecha", "Sensor", "Zona", "Temp.", "Humedad"], readings.map((reading) => {
    const sensor = CF.state.data.sensors.find((item) => Number(item.id) === Number(reading.device_id));
    return [
      CF.fmtDate(reading.recorded_at),
      CF.escapeHtml(sensor?.name || "-"),
      sensor ? CF.locationName(sensor.cold_location_id) : "-",
      reading.temperature ?? "-",
      reading.humidity ?? "-",
    ];
  }));
};

CF.readingForm = function readingForm(sensorId = null) {
  return `
    <form id="reading-form" class="form-grid">
      <label>Sensor<select name="sensor_id" required>${CF.optionList(CF.activeItems(CF.state.data.sensors), "name", sensorId)}</select></label>
      <label>Temperatura<input name="temperature" type="number" step="0.1"></label>
      <label>Humedad<input name="humidity" type="number" step="0.1"></label>
      <button class="primary-btn" type="submit">Guardar lectura</button>
    </form>
  `;
};

CF.openReadingModal = function openReadingModal(sensorId = null) {
  CF.openModal("Registrar lectura", "Si sale de rango se crea una alerta automaticamente.", CF.readingForm(sensorId), () => {
    CF.$("#reading-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = CF.formJson(event.currentTarget);
      const selectedSensorId = payload.sensor_id;
      delete payload.sensor_id;
      await CF.runAction(() => CF.api(`/sensors/${selectedSensorId}/readings`, { method: "POST", body: JSON.stringify(payload) }));
    });
  });
};

CF.coldLocationForm = function coldLocationForm(location = null) {
  const active = location ? location.is_active : true;
  const type = location?.location_type || "chamber";
  return `
    <form id="location-form" class="form-grid">
      <label>Nombre<input name="name" required value="${CF.escapeHtml(location?.name || "")}"></label>
      <label>Tipo<select name="location_type"><option value="chamber"${type === "chamber" ? " selected" : ""}>Camara</option><option value="freezer"${type === "freezer" ? " selected" : ""}>Freezer</option><option value="fridge"${type === "fridge" ? " selected" : ""}>Heladera</option><option value="warehouse"${type === "warehouse" ? " selected" : ""}>Deposito</option></select></label>
      <label>Temp. min<input name="min_temperature" type="number" step="0.1" value="${location?.min_temperature ?? ""}"></label>
      <label>Temp. max<input name="max_temperature" type="number" step="0.1" value="${location?.max_temperature ?? ""}"></label>
      <label>Humedad min<input name="min_humidity" type="number" step="0.1" value="${location?.min_humidity ?? ""}"></label>
      <label>Humedad max<input name="max_humidity" type="number" step="0.1" value="${location?.max_humidity ?? ""}"></label>
      <label>Estado<select name="is_active"><option value="true"${active ? " selected" : ""}>Activo</option><option value="false"${!active ? " selected" : ""}>Inactivo</option></select></label>
      <label class="span-2">Descripcion<textarea name="description">${CF.escapeHtml(location?.description || "")}</textarea></label>
      <button class="primary-btn" type="submit">${location ? "Guardar zona" : "Crear zona"}</button>
    </form>
  `;
};

CF.sensorForm = function sensorForm(sensor = null) {
  const active = sensor ? sensor.is_active : true;
  const type = sensor?.sensor_type || "mixed";
  return `
    <form id="sensor-form" class="form-grid">
      <label>Nombre<input name="name" required value="${CF.escapeHtml(sensor?.name || "")}"></label>
      <label>Zona<select name="cold_location_id" required>${CF.activeSelectOptions(CF.state.data.locations, sensor?.cold_location_id)}</select></label>
      <label>Tipo<select name="sensor_type"><option value="mixed"${type === "mixed" ? " selected" : ""}>Mixto</option><option value="temperature"${type === "temperature" ? " selected" : ""}>Temperatura</option><option value="humidity"${type === "humidity" ? " selected" : ""}>Humedad</option></select></label>
      <label>Estado<select name="is_active"><option value="true"${active ? " selected" : ""}>Activo</option><option value="false"${!active ? " selected" : ""}>Inactivo</option></select></label>
      <button class="primary-btn" type="submit">${sensor ? "Guardar sensor" : "Crear sensor"}</button>
    </form>
  `;
};

CF.openColdLocationModal = function openColdLocationModal(locationId = null) {
  const location = locationId ? CF.state.data.locations.find((item) => item.id === locationId) : null;
  CF.openModal(location ? "Editar camara o zona" : "Nueva camara o zona", "Define limites esperados.", CF.coldLocationForm(location), () => {
    CF.bindJsonSubmit("#location-form", location ? "PATCH" : "POST", location ? `/cold-locations/${location.id}` : "/cold-locations");
  });
};

CF.openSensorModal = function openSensorModal(sensorId = null) {
  const sensor = sensorId ? CF.state.data.sensors.find((item) => item.id === sensorId) : null;
  CF.openModal(sensor ? "Editar sensor" : "Nuevo sensor", "Asocia un dispositivo a una sola zona.", CF.sensorForm(sensor), () => {
    CF.bindJsonSubmit("#sensor-form", sensor ? "PATCH" : "POST", sensor ? `/sensors/${sensor.id}` : "/sensors");
  });
};
