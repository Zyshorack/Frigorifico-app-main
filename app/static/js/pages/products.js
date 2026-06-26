CF.renderProducts = function renderProducts() {
  CF.$("#view-products").innerHTML = `
    <div class="toolbar">
      <button class="secondary-btn toolbar-action" type="button" id="open-category">Nueva categoria</button>
      <button class="secondary-btn toolbar-action" type="button" id="open-product">Nuevo producto</button>
    </div>
    <div class="grid cols-2">
      <article class="panel">
        <div class="panel-head"><div><h2>Productos</h2><p>Listado operativo.</p></div></div>
        ${CF.table(["Codigo", "Producto", "Medida", "Categoria", "Estado", "Acciones"], CF.state.data.products.map((product) => [
          CF.escapeHtml(product.code || "-"),
          CF.escapeHtml(product.name),
          CF.formatMeasure(product.weight, product.unit),
          CF.categoryName(product.category_id),
          CF.statusPill(product.is_active ? "active" : "inactive", CF.statusLabel(product.is_active)),
          CF.actionButtons("product", product.id, product.is_active),
        ]))}
      </article>
      <article class="panel">
        <div class="panel-head"><div><h2>Categorias</h2><p>Agrupacion comercial.</p></div></div>
        ${CF.table(["Categoria", "Estado", "Acciones"], CF.state.data.categories.map((category) => [
          CF.escapeHtml(category.name),
          CF.statusPill(category.is_active ? "active" : "inactive", CF.statusLabel(category.is_active)),
          CF.actionButtons("category", category.id, category.is_active),
        ]))}
      </article>
    </div>
  `;
  CF.$("#open-category").addEventListener("click", () => CF.openCategoryModal());
  CF.$("#open-product").addEventListener("click", () => CF.openProductModal());
  CF.$$('[data-edit-product]').forEach((button) => button.addEventListener("click", () => CF.openProductModal(Number(button.dataset.editProduct))));
  CF.$$('[data-delete-product]').forEach((button) => button.addEventListener("click", () => {
    CF.confirmDelete("El producto quedara inactivo y no aparecera en el catalogo disponible. Continuar?", `/products/${button.dataset.deleteProduct}`);
  }));
  CF.$$('[data-edit-category]').forEach((button) => button.addEventListener("click", () => CF.openCategoryModal(Number(button.dataset.editCategory))));
  CF.$$('[data-delete-category]').forEach((button) => button.addEventListener("click", () => {
    CF.confirmDelete("La categoria quedara inactiva para nuevos productos. Continuar?", `/categories/${button.dataset.deleteCategory}`);
  }));
};

CF.categoryForm = function categoryForm(category = null) {
  const active = category ? category.is_active : true;
  return `
    <form id="category-form" class="form-grid">
      <label>Nombre<input name="name" required value="${CF.escapeHtml(category?.name || "")}"></label>
      <label>Estado<select name="is_active"><option value="true"${active ? " selected" : ""}>Activo</option><option value="false"${!active ? " selected" : ""}>Inactivo</option></select></label>
      <label class="span-2">Descripcion<textarea name="description">${CF.escapeHtml(category?.description || "")}</textarea></label>
      <button class="primary-btn" type="submit">${category ? "Guardar categoria" : "Crear categoria"}</button>
    </form>
  `;
};

CF.productForm = function productForm(product = null) {
  const active = product ? product.is_active : true;
  const unit = product?.unit || "kg";
  return `
    <form id="product-form" class="form-grid">
      <label>Codigo<input name="code" value="${CF.escapeHtml(product?.code || "")}" placeholder="Ej: BOV-ASADO"></label>
      <label>Nombre<input name="name" required value="${CF.escapeHtml(product?.name || "")}"></label>
      <label>Peso<input name="weight" type="number" min="0.001" step="0.001" value="${CF.escapeHtml(product?.weight || "")}" placeholder="Ej: 1"></label>
      <label>Unidad<select name="unit" required>
        <option value="kg"${unit === "kg" ? " selected" : ""}>kg</option>
        <option value="g"${unit === "g" ? " selected" : ""}>g</option>
        <option value="litros"${unit === "litros" ? " selected" : ""}>litros</option>
        <option value="unidad"${unit === "unidad" ? " selected" : ""}>unidad</option>
      </select></label>
      <label>Categoria<select name="category_id"><option value="">Sin categoria</option>${CF.activeSelectOptions(CF.state.data.categories, product?.category_id)}</select></label>
      <label>Estado<select name="is_active"><option value="true"${active ? " selected" : ""}>Activo</option><option value="false"${!active ? " selected" : ""}>Inactivo</option></select></label>
      <label class="span-2">Descripcion<textarea name="description">${CF.escapeHtml(product?.description || "")}</textarea></label>
      <button class="primary-btn" type="submit">${product ? "Guardar producto" : "Crear producto"}</button>
    </form>
  `;
};

CF.openCategoryModal = function openCategoryModal(categoryId = null) {
  const category = categoryId ? CF.state.data.categories.find((item) => item.id === categoryId) : null;
  CF.openModal(category ? "Editar categoria" : "Nueva categoria", "Agrupa productos por tipo.", CF.categoryForm(category), () => {
    CF.bindJsonSubmit("#category-form", category ? "PATCH" : "POST", category ? `/categories/${category.id}` : "/categories");
  });
};

CF.openProductModal = function openProductModal(productId = null) {
  const product = productId ? CF.state.data.products.find((item) => item.id === productId) : null;
  CF.openModal(product ? "Editar producto" : "Nuevo producto", "Producto disponible para lotes.", CF.productForm(product), () => {
    CF.bindJsonSubmit("#product-form", product ? "PATCH" : "POST", product ? `/products/${product.id}` : "/products");
  });
};
