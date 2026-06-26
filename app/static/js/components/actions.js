CF.bindSubmit = function bindSubmit(selector, path) {
  const form = CF.$(selector);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    await CF.runAction(() => CF.api(path, { method: "POST", body: JSON.stringify(CF.formJson(form)) }));
  });
};

CF.bindJsonSubmit = function bindJsonSubmit(selector, method, path) {
  const form = CF.$(selector);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    await CF.runAction(() => CF.api(path, { method, body: JSON.stringify(CF.formJson(form)) }));
  });
};

CF.runAction = async function runAction(action) {
  try {
    await action();
    CF.closeModal();
    await CF.loadAll();
  } catch (error) {
    alert(error.message);
  }
};

CF.confirmDelete = async function confirmDelete(message, path) {
  if (!confirm(message)) return;
  await CF.runAction(() => CF.api(path, { method: "DELETE" }));
};
