CF.renderCurrentView = function renderCurrentView() {
  // Mapa de pantallas. El valor de CF.state.view decide que funcion se ejecuta.
  const renderers = {
    dashboard: CF.renderDashboard,
    products: CF.renderProducts,
    items: CF.renderItems,
    stock: CF.renderStock,
    alerts: CF.renderAlerts,
    cold: CF.renderCold,
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
    products: ["Productos", "Catalogo operativo y categorias."],
    items:["Elementos", "Gestion y consulta de elementos."],
    stock: ["Stock", "Recepcion, salidas, lotes y movimientos."],
    alerts: ["Alertas", "Eventos abiertos, reconocidos y resueltos."],
    cold: ["Frio", "Camaras, sensores y lecturas."],
    users: ["Usuarios", "Administracion visible solo para admin."],
  };
  CF.$("#page-title").textContent = titles[view][0];
  CF.$("#page-subtitle").textContent = titles[view][1];
  CF.renderCurrentView();
};
