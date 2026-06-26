CF.renderCurrentView = function renderCurrentView() {
  // Mapa de pantallas. El valor de CF.state.view decide que funcion se ejecuta.
  const renderers = {
    dashboard: CF.renderDashboard,
    cold: CF.renderCold,
    stock: CF.renderStock,
    alerts: CF.renderAlerts,
    products: CF.renderProducts,
    users: CF.renderUsers,
  };
  renderers[CF.state.view]();
};

CF.navigate = function navigate(view) {
  // Regla de interfaz: solo admin puede abrir la pantalla de usuarios.
  if (view === "users" && CF.state.user.role !== "admin") view = "dashboard";
  CF.state.view = view;
  CF.$$(".nav-item").forEach((item) => item.classList.toggle("is-active", item.dataset.view === view));
  CF.$$(".view").forEach((item) => item.classList.toggle("is-active", item.id === `view-${view}`));
  const titles = {
    dashboard: ["Panel", "Resumen operativo del frigorifico."],
    cold: ["Frio", "Camaras, sensores y lecturas."],
    stock: ["Stock", "Recepcion, salidas, lotes y movimientos."],
    alerts: ["Alertas", "Eventos abiertos, reconocidos y resueltos."],
    products: ["Productos", "Catalogo operativo y categorias."],
    users: ["Usuarios", "Administracion visible solo para admin."],
  };
  CF.$("#page-title").textContent = titles[view][0];
  CF.$("#page-subtitle").textContent = titles[view][1];
  CF.renderCurrentView();
};
