// Cambiar pestañas de autenticacion
CF.$$("[data-auth-tab]").forEach((button) => {
  button.addEventListener("click", () => {
    CF.setAuthTab(button.dataset.authTab);
  });
});


// Manejo comun de errores de autenticacion
async function handleAuth(action) {
  try {
    await action();
  } catch (error) {
    CF.setAuthMessage(error.message);
  }
}


// Iniciar aplicacion
async function startApp() {
  await CF.loadAll();
  CF.showApp();
  CF.navigate("dashboard");
}


// Login
CF.$("#login-form").addEventListener("submit", (event) => {
  event.preventDefault();

  handleAuth(async () => {
    const payload = CF.formJson(event.currentTarget);

    const user = await CF.api("/users/login", {
      method: "POST",
      body: JSON.stringify(payload)
    });

    CF.state.user = user;
    localStorage.setItem("cf_user", JSON.stringify(user));

    CF.setAuthMessage("");

    await startApp();
  });
});


// Registro
CF.$("#register-form").addEventListener("submit", (event) => {
  event.preventDefault();

  handleAuth(async () => {
    const payload = CF.formJson(event.currentTarget);

    await CF.api("/users", {
      method: "POST",
      body: JSON.stringify(payload)
    });

    event.currentTarget.reset();

    CF.setAuthTab("login");
    CF.setAuthMessage("Usuario creado. Ahora inicia sesion.", true);
  });
});


// Navegacion lateral
CF.$$(".nav-item").forEach((button) => {
  button.addEventListener("click", () => {
    CF.navigate(button.dataset.view);
  });
});


// Refrescar
CF.$("#refresh-btn").addEventListener("click", () => {
  CF.loadAll();
});


// Cerrar sesion
function logout() {
  localStorage.removeItem("cf_user");
  CF.state.user = null;
  CF.showAuth();
}

CF.$("#logout-btn").addEventListener("click", logout);


// Notificaciones
CF.$("#bell-btn").addEventListener("click", () => {
  CF.$("#notification-popover").classList.toggle("hidden");
});


CF.$("#go-alerts-btn").addEventListener("click", () => {
  CF.$("#notification-popover").classList.add("hidden");
  CF.navigate("alerts");
});


// Modal
CF.$("#modal-close").addEventListener("click", CF.closeModal);
CF.$(".modal-backdrop").addEventListener("click", CF.closeModal);


// Arranque
if (CF.state.user) {

  startApp().catch(() => {
    logout();
  });

} else {

  CF.showAuth();

}