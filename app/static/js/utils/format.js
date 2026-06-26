CF.escapeHtml = function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
};

CF.fmtDate = function fmtDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" });
};

CF.formJson = function formJson(form) {
  const payload = {};
  new FormData(form).forEach((value, key) => {
    if (value === "") return;
    if (["quantity", "remaining_quantity", "weight", "temperature", "humidity", "min_temperature", "max_temperature", "min_humidity", "max_humidity"].includes(key)) {
      payload[key] = Number(value);
      return;
    }
    if (["product_id", "category_id", "cold_location_id", "user_id", "sensor_id", "device_id"].includes(key)) {
      payload[key] = Number(value);
      return;
    }
    if (key === "is_active") {
      payload[key] = value === "true" || value === "on";
      return;
    }
    payload[key] = value;
  });
  return payload;
};

CF.isActive = function isActive(item) {
  return item && item.is_active !== false;
};

CF.activeItems = function activeItems(items) {
  return items.filter(CF.isActive);
};

CF.optionList = function optionList(items, labelKey = "name", selectedId = null) {
  return items.map((item) => {
    const selected = Number(selectedId) === Number(item.id) ? " selected" : "";
    return `<option value="${item.id}"${selected}>${CF.escapeHtml(item[labelKey])}</option>`;
  }).join("");
};

CF.activeSelectOptions = function activeSelectOptions(items, selectedId = null) {
  const selectedItem = items.find((item) => Number(item.id) === Number(selectedId));
  const active = CF.activeItems(items);
  const source = selectedItem && !CF.isActive(selectedItem) ? [selectedItem, ...active] : active;
  return CF.optionList(source, "name", selectedId);
};

CF.statusLabel = function statusLabel(value) {
  return value ? "Activo" : "Inactivo";
};

CF.statusPill = function statusPill(value, label = null) {
  return `<span class="status-pill ${CF.escapeHtml(String(value))}">${CF.escapeHtml(label || value)}</span>`;
};

CF.actionButtons = function actionButtons(kind, id, canDelete = true) {
  return `
    <div class="table-actions">
      <button class="secondary-btn compact-btn" data-edit-${kind}="${id}" type="button">Editar</button>
      ${canDelete ? `<button class="danger-btn compact-btn" data-delete-${kind}="${id}" type="button">Borrar</button>` : ""}
    </div>
  `;
};

CF.table = function table(headers, rows) {
  if (!rows.length) return `<div class="empty">Sin datos cargados.</div>`;
  return `
    <div class="table-wrap">
      <table>
        <thead><tr>${headers.map((header) => `<th>${CF.escapeHtml(header)}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows.map((row) => `<tr>${row.map((cell) => `<td>${cell ?? ""}</td>`).join("")}</tr>`).join("")}
        </tbody>
      </table>
    </div>
  `;
};

CF.statCard = function statCard(title, value, subtitle) {
  return `<article class="stat-card"><h3>${CF.escapeHtml(title)}</h3><p>${CF.escapeHtml(subtitle)}</p><div class="stat-value">${CF.escapeHtml(value)}</div></article>`;
};

CF.categoryName = function categoryName(id) {
  return CF.escapeHtml(CF.state.data.categories.find((item) => item.id === id)?.name || "-");
};

CF.productName = function productName(id) {
  return CF.escapeHtml(CF.state.data.products.find((item) => item.id === id)?.name || "-");
};

CF.locationName = function locationName(id) {
  return CF.escapeHtml(CF.state.data.locations.find((item) => item.id === id)?.name || "-");
};

CF.userName = function userName(id, fallback = null) {
  return CF.escapeHtml(fallback || CF.state.data.users.find((item) => Number(item.id) === Number(id))?.username || "-");
};

CF.formatMeasure = function formatMeasure(weight, unit) {
  if (weight === null || weight === undefined || weight === "") return CF.escapeHtml(unit || "-");
  return `${CF.escapeHtml(weight)} ${CF.escapeHtml(unit || "")}`.trim();
};

CF.renderCatalogTable = function renderCatalogTable(items) {
  if (!items.length) return `<div class="empty">Sin productos disponibles todavia.</div>`;
  return CF.table(["Producto", "Codigo", "Medida", "Disponible"], items.map((product) => [
    CF.escapeHtml(product.name),
    CF.escapeHtml(product.code || "-"),
    CF.formatMeasure(product.weight, product.unit),
    product.available_quantity,
  ]));
};

CF.alertActionButtons = function alertActionButtons(alert) {
  if (alert.status === "resolved") return "";
  return `
    <div class="table-actions">
      <button class="primary-btn compact-btn" data-resolve-alert="${alert.id}" type="button">Resolver</button>
    </div>
  `;
};

CF.renderAlertRows = function renderAlertRows(alerts, withActions = false) {
  if (!alerts.length) return `<div class="empty">No hay alertas para mostrar.</div>`;
  return CF.table(["Tipo", "Severidad", "Estado", "Mensaje", "Fecha", "Resolucion", withActions ? "Acciones" : ""], alerts.map((alert) => [
    CF.escapeHtml(alert.alert_type),
    CF.statusPill(alert.severity),
    CF.statusPill(alert.status),
    CF.escapeHtml(alert.message),
    CF.fmtDate(alert.created_at),
    alert.status === "resolved"
      ? `${CF.escapeHtml(alert.action_description || "-")}<br><small>${CF.fmtDate(alert.resolved_at)} · ${CF.userName(alert.resolved_by_user_id, alert.resolved_by_username)}</small>`
      : "-",
    withActions ? CF.alertActionButtons(alert) : "",
  ]));
};
