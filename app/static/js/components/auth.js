CF.setAuthMessage = function setAuthMessage(message, ok = false) {
  const target = CF.$("#auth-message");
  target.textContent = message;
  target.classList.toggle("ok", ok);
};

CF.showAuth = function showAuth() {
  CF.$("#auth-screen").classList.remove("hidden");
  CF.$("#app-screen").classList.add("hidden");
};

CF.showApp = function showApp() {
  CF.$("#auth-screen").classList.add("hidden");
  CF.$("#app-screen").classList.remove("hidden");
  CF.$("#role-label").textContent = `${CF.state.user.username} - ${CF.state.user.role}`;
  CF.$$(".admin-only").forEach((item) => item.classList.toggle("hidden", CF.state.user.role !== "admin"));
  CF.loadAll();
};

CF.setAuthTab = function setAuthTab(tab) {
  CF.$$("[data-auth-tab]").forEach((button) => button.classList.toggle("is-active", button.dataset.authTab === tab));
  CF.$("#login-form").classList.toggle("hidden", tab !== "login");
  CF.$("#register-form").classList.toggle("hidden", tab !== "register");
  CF.setAuthMessage("");
};
