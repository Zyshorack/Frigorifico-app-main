CF.state.stockTab = CF.state.stockTab || "summary";

CF.renderStock = function renderStock() {
  const tab = CF.state.stockTab || "summary";
  CF.$("#view-stock").innerHTML = `
    <div class="toolbar split-toolbar">
      <div class="segmented-control" role="group" aria-label="Secciones de stock">
        ${CF.stockTabButton("summary", "Resumen", tab)}
        ${CF.stockTabButton("reception", "Recepcion", tab)}
        ${CF.stockTabButton("exit", "Salida", tab)}
        ${CF.stockTabButton("batches", "Lotes", tab)}
        ${CF.stockTabButton("movements", "Movimientos", tab)}
      </div>
    </div>
    ${CF.renderStockTab(tab)}
  `;

  CF.$$('[data-stock-tab]').forEach((button) => button.addEventListener("click", () => {
    CF.state.stockTab = button.dataset.stockTab;
    CF.renderStock();
  }));
  CF.bindStockTabActions(tab);
};

CF.stockTabButton = function stockTabButton(value, label, activeTab) {
  return `<button class="segment-btn ${activeTab === value ? "is-active" : ""}" type="button" data-stock-tab="${value}">${label}</button>`;
};

CF.renderStockTab = function renderStockTab(tab) {
  const renderers = {
    summary: CF.renderStockSummary,
    reception: CF.renderStockReception,
    exit: CF.renderStockExit,
    batches: CF.renderStockBatches,
    movements: CF.renderStockMovements,
  };
  return (renderers[tab] || CF.renderStockSummary)();
};

CF.bindStockTabActions = function bindStockTabActions(tab) {
  if (tab === "reception") CF.bindJsonSubmit("#stock-entry-form", "POST", "/stock/entry");
  if (tab === "exit") CF.bindJsonSubmit("#stock-exit-form", "POST", "/stock/exit");
  if (tab === "batches") {
    CF.$$('[data-edit-batch]').forEach((button) => button.addEventListener("click", () => CF.openBatchEditModal(Number(button.dataset.editBatch))));
    CF.$$('[data-delete-batch]').forEach((button) => button.addEventListener("click", () => {
      CF.confirmDelete("El lote quedara descartado y saldra del stock disponible. Continuar?", `/stock/batches/${button.dataset.deleteBatch}`);
    }));
  }
};

CF.activeBatches = function activeBatches() {
  return CF.state.data.batches.filter((batch) => batch.status === "active" && batch.remaining_quantity > 0);
};

CF.expiringBatches = function expiringBatches(days = 7) {
  const today = new Date();
  const limit = new Date();
  limit.setDate(today.getDate() + days);
  return CF.activeBatches().filter((batch) => {
    const expires = new Date(`${batch.expiration_date}T00:00:00`);
    return expires >= today && expires <= limit;
  });
};

CF.renderStockSummary = function renderStockSummary() {
  const activeBatches = CF.activeBatches();
  const expiring = CF.expiringBatches(7);
  const totalUnits = activeBatches.reduce((total, batch) => total + Number(batch.remaining_quantity || 0), 0);
  return `
    <div class="grid cols-3">
      ${CF.statCard("Productos con stock", CF.state.data.catalog.filter((item) => item.available_quantity > 0).length, "Catalogo disponible")}
      ${CF.statCard("Lotes activos", activeBatches.length, "Partidas disponibles")}
      ${CF.statCard("Por vencer", expiring.length, "Proximos 7 dias")}
    </div>
    <div class="grid cols-2" style="margin-top:14px">
      <article class="panel">
        <div class="panel-head"><div><h2>Disponibilidad</h2><p>Stock activo por producto.</p></div></div>
        ${CF.renderCatalogTable(CF.state.data.catalog)}
      </article>
      <article class="panel">
        <div class="panel-head"><div><h2>Vencimientos cercanos</h2><p>Lotes que conviene mover primero.</p></div></div>
        ${CF.renderBatchTable(expiring, false)}
      </article>
    </div>
  `;
};

CF.renderStockReception = function renderStockReception() {
  return `
    <article class="panel user-admin-panel">
      <div class="panel-head"><div><h2>Recepcion</h2><p>Registra mercaderia que ingresa y crea un lote.</p></div></div>
      ${CF.stockEntryForm()}
    </article>
  `;
};

CF.renderStockExit = function renderStockExit() {
  return `
    <article class="panel user-admin-panel">
      <div class="panel-head"><div><h2>Salida</h2><p>Descuenta stock usando FEFO: primero vence, primero sale.</p></div></div>
      ${CF.stockExitForm()}
    </article>
  `;
};

CF.renderStockBatches = function renderStockBatches() {
  return `
    <article class="panel">
      <div class="panel-head"><div><h2>Lotes</h2><p>Existencia real por partida, proveedor y vencimiento.</p></div></div>
      ${CF.renderBatchTable(CF.state.data.batches, true)}
    </article>
  `;
};

CF.renderStockMovements = function renderStockMovements() {
  return `
    <article class="panel">
      <div class="panel-head"><div><h2>Movimientos</h2><p>Historial de entradas, salidas y ajustes.</p></div></div>
      ${CF.renderMovementTable(CF.state.data.movements)}
    </article>
  `;
};

CF.stockEntryForm = function stockEntryForm() {
  return `
    <form id="stock-entry-form" class="form-grid">
      <input type="hidden" name="user_id" value="${CF.state.user?.id || ""}">
      <label>Producto<select name="product_id" required>${CF.optionList(CF.activeItems(CF.state.data.products))}</select></label>
      <label>Camara<select name="cold_location_id"><option value="">Sin camara</option>${CF.optionList(CF.activeItems(CF.state.data.locations))}</select></label>
      <label>Cantidad<input name="quantity" type="number" min="0.01" step="0.01" required></label>
      <label>Vencimiento<input name="expiration_date" type="date" required></label>
      <label class="span-2">Proveedor<input name="supplier" maxlength="120" placeholder="Nombre del proveedor del lote"></label>
      <label class="span-2">Remito o factura<input name="document_number" maxlength="120" placeholder="Ej: R-0001-00012345"></label>
      <label class="span-2">Detalle<textarea name="description" placeholder="Remito, factura u observacion de recepcion"></textarea></label>
      <button class="primary-btn" type="submit">Registrar entrada</button>
    </form>
  `;
};

CF.stockExitForm = function stockExitForm() {
  return `
    <form id="stock-exit-form" class="form-grid">
      <input type="hidden" name="user_id" value="${CF.state.user?.id || ""}">
      <label>Producto<select name="product_id" required>${CF.optionList(CF.activeItems(CF.state.data.products))}</select></label>
      <label>Camara<select name="cold_location_id"><option value="">Cualquier camara</option>${CF.optionList(CF.activeItems(CF.state.data.locations))}</select></label>
      <label>Cantidad<input name="quantity" type="number" min="0.01" step="0.01" required></label>
      <label class="span-2">Detalle<textarea name="description" placeholder="Destino, cliente o motivo de salida"></textarea></label>
      <button class="primary-btn" type="submit">Registrar salida</button>
    </form>
  `;
};

CF.renderBatchTable = function renderBatchTable(batches, withActions) {
  return CF.table(["Producto", "Proveedor", "Comprobante", "Camara", "Inicial", "Restante", "Vence", "Estado", withActions ? "Acciones" : ""], batches.map((batch) => [
    CF.productName(batch.product_id),
    CF.escapeHtml(batch.supplier || "-"),
    CF.escapeHtml(batch.document_number || "-"),
    CF.locationName(batch.cold_location_id),
    batch.quantity,
    batch.remaining_quantity,
    batch.expiration_date,
    CF.statusPill(batch.status),
    withActions ? CF.actionButtons("batch", batch.id, batch.status !== "discarded") : "",
  ]));
};

CF.renderMovementTable = function renderMovementTable(movements) {
  return CF.table(["Fecha", "Tipo", "Producto", "Lote", "Camara", "Cantidad", "Usuario", "Detalle"], movements.map((movement) => [
    CF.fmtDate(movement.created_at),
    CF.statusPill(movement.movement_type),
    CF.productName(movement.product_id),
    movement.batch_id,
    CF.locationName(movement.cold_location_id),
    movement.quantity,
    CF.userName(movement.user_id, movement.user_name),
    CF.escapeHtml(movement.description || "-"),
  ]));
};

CF.openBatchEditModal = function openBatchEditModal(batchId) {
  const batch = CF.state.data.batches.find((item) => item.id === batchId);
  if (!batch) return;
  CF.openModal("Editar lote", "Ajusta ubicacion, vencimiento o estado.", `
    <form id="batch-form" class="form-grid">
      <label>Producto<input value="${CF.productName(batch.product_id)}" disabled></label>
      <label>Camara<select name="cold_location_id"><option value="">Sin camara</option>${CF.activeSelectOptions(CF.state.data.locations, batch.cold_location_id)}</select></label>
      <label>Restante<input name="remaining_quantity" type="number" min="0" max="${batch.quantity}" step="0.01" value="${batch.remaining_quantity}" required></label>
      <label>Vencimiento<input name="expiration_date" type="date" value="${batch.expiration_date}" required></label>
      <label>Proveedor<input name="supplier" maxlength="120" value="${CF.escapeHtml(batch.supplier || "")}"></label>
      <label>Remito o factura<input name="document_number" maxlength="120" value="${CF.escapeHtml(batch.document_number || "")}"></label>
      <label>Estado<select name="status">
        <option value="active"${batch.status === "active" ? " selected" : ""}>Activo</option>
        <option value="exhausted"${batch.status === "exhausted" ? " selected" : ""}>Agotado</option>
        <option value="expired"${batch.status === "expired" ? " selected" : ""}>Vencido</option>
        <option value="quarantined"${batch.status === "quarantined" ? " selected" : ""}>Cuarentena</option>
        <option value="discarded"${batch.status === "discarded" ? " selected" : ""}>Descartado</option>
      </select></label>
      <button class="primary-btn" type="submit">Guardar lote</button>
    </form>
  `, () => CF.bindJsonSubmit("#batch-form", "PATCH", `/stock/batches/${batch.id}`));
};
