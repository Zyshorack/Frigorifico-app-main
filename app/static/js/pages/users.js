CF.state.userFilter = CF.state.userFilter || "active";

CF.renderUsers = function renderUsers() {

    if (CF.state.user.role !== "admin") {

        CF.$("#view-users").innerHTML = `
            <div class="empty">
                Este apartado solo está disponible para administradores.
            </div>
        `;

        return;
    }

    const filter = CF.state.userFilter || "active";
    const users = CF.filteredUsers(filter);

    CF.$("#view-users").innerHTML = `
        <div class="toolbar split-toolbar">

            <div class="segmented-control" role="group" aria-label="Filtrar usuarios">

                <button 
                    class="segment-btn ${filter === "active" ? "is-active" : ""}" 
                    type="button" 
                    data-user-filter="active">
                    Activos
                </button>

                <button 
                    class="segment-btn ${filter === "inactive" ? "is-active" : ""}" 
                    type="button" 
                    data-user-filter="inactive">
                    Inactivos
                </button>

                <button 
                    class="segment-btn ${filter === "history" ? "is-active" : ""}" 
                    type="button" 
                    data-user-filter="history">
                    Historial
                </button>

            </div>

            <button 
                class="secondary-btn toolbar-action" 
                type="button" 
                id="open-user-create">
                Crear usuario
            </button>

        </div>


        <article class="panel">

            ${CF.table(
                ["Usuario", "Rol", "Estado", "Alta", "Acciones"],

                users.map((user) => [

                    CF.escapeHtml(user.username),

                    CF.escapeHtml(user.role),

                    CF.statusPill(
                        user.is_active ? "active" : "inactive",
                        CF.statusLabel(user.is_active)
                    ),

                    CF.fmtDate(user.created_at),

                    CF.userActionButtons(user)

                ])
            )}

        </article>
    `;


    // filtros

    CF.$$('[data-user-filter]').forEach((button) => {

        button.addEventListener("click", () => {

            CF.state.userFilter = button.dataset.userFilter;

            CF.renderUsers();

        });

    });


    // crear

    CF.$("#open-user-create")
        .addEventListener(
            "click",
            CF.openUserCreateModal
        );


    // editar

    CF.$$('[data-edit-user]').forEach((button) => {

        button.addEventListener("click", () => {

            CF.openUserEditModal(
                Number(button.dataset.editUser)
            );

        });

    });


    // desactivar

    CF.$$('[data-disable-user]').forEach((button) => {

        button.addEventListener("click", () => {

            CF.confirmDelete(
                "El usuario quedara inactivo. Continuar?",
                `/users/${button.dataset.disableUser}`
            );

        });

    });


    // reactivar

    CF.$$('[data-reactivate-user]').forEach((button) => {

        button.addEventListener("click", async () => {

            await CF.api(
                `/users/${button.dataset.reactivateUser}`,
                {
                    method: "PATCH",
                    body: JSON.stringify({
                        is_active: true
                    })
                }
            );

            await CF.loadAll();

            CF.state.userFilter = "active";

            CF.renderUsers();

        });

    });


    // eliminar permanente

    CF.$$('[data-delete-user-permanent]').forEach((button) => {

        button.addEventListener("click", () => {

            CF.confirmDelete(
                "El usuario sera eliminado definitivamente de la base de datos. Continuar?",
                `/users/${button.dataset.deleteUserPermanent}/permanent`
            );

        });

    });

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

CF.itemForm = function(item = null) {
  return `
    <form id="${item ? "edit-item-form" : "create-item-form"}" class="form-grid">

      <label>
        Nombre
        <input
          name="name"
          required
          value="${CF.escapeHtml(item?.name || "")}">
      </label>

      <label>
        Descripción
        <textarea
          name="description">${CF.escapeHtml(item?.description || "")}</textarea>
      </label>

      <button class="primary-btn" type="submit">
        ${item ? "Guardar cambios" : "Crear elemento"}
      </button>

    </form>
  `;
};

CF.openItemCreateModal = function () {
    CF.openModal(
        "Crear elemento",
        "Alta de un nuevo elemento.",
        CF.itemForm(),
        () => {
            CF.bindJsonSubmit(
                "#create-item-form",
                "POST",
                "/items"
            );
        }
    );
};

CF.openItemEditModal = function(id) {

    const item = CF.state.data.items.find(i => i.id === id);

    if (!item) return;

    CF.openModal(
        "Editar elemento",
        "",
        CF.itemForm(item),
        () => {
            CF.bindJsonSubmit(
                "#edit-item-form",
                "PATCH",
                `/items/${id}`
            );
        }
    );
};

CF.renderItems = function renderItems() {

    const isAdmin = CF.state.user.role === "admin";

    const items = [...CF.state.data.items]
        .filter(item => isAdmin || item.is_active)
        .sort((a, b) => a.name.localeCompare(b.name));

    CF.$("#view-items").innerHTML = `
        ${isAdmin ? `
            <div class="toolbar">
                <button
                    class="secondary-btn"
                    id="open-item-create">
                    Crear elemento
                </button>
            </div>
        ` : ""}

        <article class="panel">

            ${CF.table(

                isAdmin
                    ? ["Nombre","Descripción","Estado","Fecha","Acciones"]
                    : ["Nombre","Descripción","Fecha"],

                items.map(item =>

                    isAdmin

                    ? [

                        CF.escapeHtml(item.name),

                        CF.escapeHtml(item.description),

                        CF.statusPill(
                            item.is_active ? "active" : "inactive",
                            CF.statusLabel(item.is_active)
                        ),

                        CF.fmtDate(item.created_at),

                        CF.actionButtons(
                            "item",
                            item.id,
                            item.is_active
                        )

                    ]

                    : [

                        CF.escapeHtml(item.name),

                        CF.escapeHtml(item.description),

                        CF.fmtDate(item.created_at)

                    ]

                )

            )}

        </article>
    `;

    if (!isAdmin) return;

    CF.$("#open-item-create")
        .addEventListener("click", CF.openItemCreateModal);

    CF.$$("[data-edit-item]").forEach(button =>
        button.addEventListener("click", () =>
            CF.openItemEditModal(Number(button.dataset.editItem))
        )
    );

    CF.$$("[data-delete-item]").forEach(button =>
        button.addEventListener("click", () =>
            CF.confirmDelete(
                "El elemento quedará inactivo. ¿Continuar?",
                `/items/${button.dataset.deleteItem}`
            )
        )
    );

};

CF.userActionButtons = function userActionButtons(user) {
  return `
    <div class="table-actions">

      <button 
        class="secondary-btn compact-btn" 
        data-edit-user="${user.id}" 
        type="button">
        Editar
      </button>

      ${
        user.is_active
        ? `
          <button 
            class="secondary-btn compact-btn" 
            data-disable-user="${user.id}" 
            type="button">
            Desactivar
          </button>
        `
        :
        `
          <button 
            class="secondary-btn compact-btn" 
            data-reactivate-user="${user.id}" 
            type="button">
            Activar
          </button>
        `
      }

      <button 
        class="danger-btn compact-btn" 
        data-delete-user-permanent="${user.id}" 
        type="button">
        Eliminar
      </button>

    </div>
  `;
};