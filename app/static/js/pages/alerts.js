CF.state.alertFilter = CF.state.alertFilter || "active";

CF.renderAlerts = function renderAlerts() {
  const filter = CF.state.alertFilter || "active";
  const visibleAlerts = CF.filteredAlerts(filter);
  CF.$("#view-alerts").innerHTML = `
    <div class="toolbar split-toolbar">
      <div class="segmented-control" role="group" aria-label="Filtrar alertas">
        <button class="segment-btn ${filter === "active" ? "is-active" : ""}" type="button" data-alert-filter="active">Activas</button>
        <button class="segment-btn ${filter === "resolved" ? "is-active" : ""}" type="button" data-alert-filter="resolved">Resueltas</button>
        <button class="segment-btn ${filter === "history" ? "is-active" : ""}" type="button" data-alert-filter="history">Historial</button>
      </div>
    </div>
    <article class="panel">
      <div class="panel-head">
        <div><h2>Alertas</h2><p>Eventos manuales y automaticos con evidencia operativa.</p></div>
      </div>
      ${CF.renderAlertRows(visibleAlerts, true)}
    </article>
  `;
  CF.$$('[data-alert-filter]').forEach((button) => button.addEventListener("click", () => {
    CF.state.alertFilter = button.dataset.alertFilter;
    CF.renderAlerts();
  }));
  CF.$$('[data-resolve-alert]').forEach((button) => {
    button.addEventListener("click", () => CF.openResolveAlertModal(Number(button.dataset.resolveAlert)));
  });
};

CF.filteredAlerts = function filteredAlerts(filter) {
  const alerts = [...CF.state.data.alerts].filter((alert) => alert.is_active !== false).sort((left, right) => new Date(right.created_at) - new Date(left.created_at));
  if (filter === "active") return alerts.filter((alert) => alert.status !== "resolved");
  if (filter === "resolved") return alerts.filter((alert) => alert.status === "resolved");
  if (filter === "history") return alerts;
  return alerts.filter((alert) => alert.status !== "resolved");
};

CF.openResolveAlertModal = function openResolveAlertModal(alertId) {
  CF.openModal("Resolver alerta", "Agrega evidencia antes de cerrar el evento.", `
    <form id="resolve-alert-form" class="form-grid">
      <input type="hidden" name="status" value="resolved">
      <input type="hidden" name="user_id" value="${CF.state.user.id}">
      <label class="span-2">Accion correctiva<textarea name="action_description" required minlength="3"></textarea></label>
      <button class="primary-btn" type="submit">Resolver alerta</button>
    </form>
  `, () => {
    CF.$("#resolve-alert-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      await CF.runAction(() => CF.api(`/alerts/${alertId}/status`, { method: "PATCH", body: JSON.stringify(CF.formJson(event.currentTarget)) }));
    });
  });
};
