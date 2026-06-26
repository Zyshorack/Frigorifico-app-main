CF.state.userFilter = CF.state.userFilter || "active";

CF.renderUsers = function renderUsers() {
  if (CF.state.user.role !== "admin") {
    CF.$("#view-users").innerHTML = `<div class="empty">Este apartado solo lo ve un admin.</div>`;
    return;
  }

  const filter = CF.state.userFilter || "active";
  const users = CF.filteredUsers(filter);
  CF.$("#view-users").innerHTML = `
    <div class="toolbar split-toolbar">
      <div class="segmented-control" role="group" aria-label="Filtrar usuarios">
        <button class="segment-btn ${filter === "active" ? "is-active" : ""}" type="button" data-user-filter="active">Activos</button>
        <button class="segment-btn ${filter === "inactive" ? "is-active" : ""}" type="button" data-user-filter="inactive">Inactivos</button>
        <button class="segment-btn ${filter === "history" ? "is-active" : ""}" type="button" data-user-filter="history">Historial</button>
      </div>
      <button class="secondary-btn toolbar-action" type="button" id="open-user-create">Crear usuario</button>
    </div>
    <article class="panel">
      ${CF.table(["Usuario", "Rol", "Estado", "Alta", "Acciones"], users.map((user) => [
        CF.escapeHtml(user.username),
        CF.escapeHtml(user.role),
        CF.statusPill(user.is_active ? "active" : "inactive", CF.statusLabel(user.is_active)),
        CF.fmtDate(user.created_at),
        CF.actionButtons("user", user.id, user.is_active),
      ]))}
    </article>
  `;

  CF.$$('[data-user-filter]').forEach((button) => button.addEventListener("click", () => {
    CF.state.userFilter = button.dataset.userFilter;
    CF.renderUsers();
  }));
  CF.$("#open-user-create").addEventListener("click", CF.openUserCreateModal);
  CF.$$('[data-edit-user]').forEach((button) => button.addEventListener("click", () => CF.openUserEditModal(Number(button.dataset.editUser))));
  CF.$$('[data-delete-user]').forEach((button) => button.addEventListener("click", () => {
    CF.confirmDelete("El usuario quedara inactivo. Continuar?", `/users/${button.dataset.deleteUser}`);
  }));
};

CF.filteredUsers = function filteredUsers(filter) {
  const users = [...CF.state.data.users].sort((left, right) => left.username.localeCompare(right.username));
  if (filter === "active") return users.filter((user) => user.is_active);
  if (filter === "inactive") return users.filter((user) => !user.is_active);
  return users;
};

CF.userForm = function userForm(user = null) {
  const active = user ? user.is_active : true;
  return `
    <form id="${user ? "edit-user-form" : "create-user-form"}" class="form-grid">
      <label>Usuario<input name="username" required minlength="3" value="${CF.escapeHtml(user?.username || "")}"></label>
      <label>${user ? "Nueva contrasena" : "Contrasena"}<input name="password" type="password" ${user ? 'placeholder="Sin cambios"' : "required"} minlength="6"></label>
      <label>Rol<select name="role">
        <option value="operator"${user?.role === "operator" ? " selected" : ""}>Operador</option>
        <option value="admin"${user?.role === "admin" ? " selected" : ""}>Admin</option>
        <option value="client"${user?.role === "client" ? " selected" : ""}>Cliente</option>
      </select></label>
      ${user ? `<label>Estado<select name="is_active">
        <option value="true"${active ? " selected" : ""}>Activo</option>
        <option value="false"${!active ? " selected" : ""}>Inactivo</option>
      </select></label>` : ""}
      <button class="primary-btn" type="submit">${user ? "Guardar cambios" : "Crear usuario"}</button>
    </form>
  `;
};

CF.openUserCreateModal = function openUserCreateModal() {
  CF.openModal("Crear usuario", "Alta de usuario para acceder al sistema.", CF.userForm(), () => {
    CF.bindJsonSubmit("#create-user-form", "POST", "/users");
  });
};

CF.openUserEditModal = function openUserEditModal(userId) {
  const user = CF.state.data.users.find((item) => item.id === userId);
  if (!user) return;
  CF.openModal("Editar usuario", "Actualiza rol, estado o credenciales.", CF.userForm(user), () => {
    CF.bindJsonSubmit("#edit-user-form", "PATCH", `/users/${userId}`);
  });
};
