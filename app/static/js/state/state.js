localStorage.removeItem("cf_demo_mode");
localStorage.removeItem("cf_demo_accounts");

CF.state = {
  // Usuario logueado. Se guarda en localStorage para no perder la sesion al recargar.
  user: JSON.parse(localStorage.getItem("cf_user") || "null"),
  view: "dashboard",
  data: {
    users: [],
    categories: [],
    products: [],
    catalog: [],
    locations: [],
    sensors: [],
    readings: [],
    batches: [],
    movements: [],
    alerts: [],
  },
};
