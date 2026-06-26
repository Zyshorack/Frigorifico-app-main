CF.api = async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) {
    const detail = data && data.detail ? data.detail : "No se pudo completar la operacion.";
    throw new Error(detail);
  }
  return data;
};

CF.loadAll = async function loadAll() {
  // Refresca los datos compartidos por todas las pantallas antes de renderizar.
  const requests = [
    CF.api("/categories").then((data) => (CF.state.data.categories = data)),
    CF.api("/products").then((data) => (CF.state.data.products = data)),
    CF.api("/catalog").then((data) => (CF.state.data.catalog = data)),
    CF.api("/cold-locations").then((data) => (CF.state.data.locations = data)),
    CF.api("/sensors").then((data) => (CF.state.data.sensors = data)),
    CF.api("/sensor-readings").then((data) => (CF.state.data.readings = data)),
    CF.api("/stock/batches").then((data) => (CF.state.data.batches = data)),
    CF.api("/stock/movements").then((data) => (CF.state.data.movements = data)),
    CF.api("/alerts").then((data) => (CF.state.data.alerts = data)),
  ];
  if (CF.state.user && CF.state.user.role === "admin") {
    // Usuarios solo se carga para admin porque es informacion administrativa.
    requests.push(CF.api("/users").then((data) => (CF.state.data.users = data)));
  }
  await Promise.allSettled(requests);
  CF.updateNotifications();
  CF.renderCurrentView();
};
