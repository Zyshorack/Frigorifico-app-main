CF.openModal = function openModal(title, subtitle, body, onReady) {
  CF.$("#modal-title").textContent = title;
  CF.$("#modal-subtitle").textContent = subtitle;
  CF.$("#modal-body").innerHTML = body;
  CF.$("#modal-root").classList.remove("hidden");
  if (onReady) onReady();
};

CF.closeModal = function closeModal() {
  CF.$("#modal-root").classList.add("hidden");
  CF.$("#modal-body").innerHTML = "";
};
