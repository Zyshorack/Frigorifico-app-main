CF.renderDashboard = function renderDashboard() {
  const openAlerts = CF.state.data.alerts.filter((alert) => alert.status === "open");
  const activeProducts = CF.activeItems(CF.state.data.products);
  const activeBatches = CF.state.data.batches.filter((batch) => batch.status === "active");
  CF.$("#view-dashboard").innerHTML = `
    <div class="grid cols-3">
      ${CF.statCard("Alertas abiertas", openAlerts.length, "Lecturas o eventos pendientes.")}
      ${CF.statCard("Productos activos", activeProducts.length, "Catalogo disponible.")}
      ${CF.statCard("Lotes activos", activeBatches.length, "Stock utilizable.")}
    </div>
    <div class="grid cols-2" style="margin-top:14px">
      <article class="panel">
        <div class="panel-head">
          <div><h2>Ultimas alertas</h2><p>La campana toma estos eventos abiertos.</p></div>
          <button class="secondary-btn" type="button" data-jump="alerts">Ir a alertas</button>
        </div>
        ${CF.renderAlertRows(openAlerts.slice(0, 5))}
      </article>
      <article class="panel">
        <div class="panel-head">
          <div><h2>Disponibilidad</h2><p>Stock activo y no vencido por producto.</p></div>
          <button class="secondary-btn" type="button" data-jump="stock">Gestionar stock</button>
        </div>
        ${CF.renderCatalogTable(CF.state.data.catalog.slice(0, 5))}
      </article>
    </div>
  `;
  CF.$$('[data-jump]').forEach((button) => button.addEventListener("click", () => CF.navigate(button.dataset.jump)));
};
