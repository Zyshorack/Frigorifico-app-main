CF.$$("[data-auth-tab]").forEach((button) => button.addEventListener("click", () => CF.setAuthTab(button.dataset.authTab)));

CF.$("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const payload = CF.formJson(event.currentTarget);
    const user = await CF.api("/users/login", { method: "POST", body: JSON.stringify(payload) });
    CF.state.user = user;
    localStorage.setItem("cf_user", JSON.stringify(user));
    CF.setAuthMessage("");
    CF.showApp();
  } catch (error) {
    CF.setAuthMessage(error.message);
  }
});

// Registro simple contra el backend real.
CF.$("#register-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await CF.api("/users", { method: "POST", body: JSON.stringify(CF.formJson(event.currentTarget)) });
    event.currentTarget.reset();
    CF.setAuthTab("login");
    CF.setAuthMessage("Usuario creado. Ahora inicia sesion.", true);
  } catch (error) {
    CF.setAuthMessage(error.message);
  }
});

// Eventos globales: navegacion lateral, refresco, salir, campana y modal.
CF.$$(".nav-item").forEach((button) => button.addEventListener("click", () => CF.navigate(button.dataset.view)));
CF.$("#refresh-btn").addEventListener("click", CF.loadAll);
CF.$("#logout-btn").addEventListener("click", () => {
  localStorage.removeItem("cf_user");
  CF.state.user = null;
  CF.showAuth();
});
CF.$("#bell-btn").addEventListener("click", () => CF.$("#notification-popover").classList.toggle("hidden"));
CF.$("#go-alerts-btn").addEventListener("click", () => {
  CF.$("#notification-popover").classList.add("hidden");
  CF.navigate("alerts");
});
CF.$("#modal-close").addEventListener("click", CF.closeModal);
CF.$(".modal-backdrop").addEventListener("click", CF.closeModal);

// Punto de arranque: muestra la app si habia sesion guardada, o el login si no.
if (CF.state.user) {
  CF.showApp();
} else {
  CF.showAuth();
}
