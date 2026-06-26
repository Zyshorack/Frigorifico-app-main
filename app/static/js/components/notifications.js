CF.updateNotifications = function updateNotifications() {
  const openAlerts = CF.state.data.alerts.filter((alert) => alert.status === "open");
  const count = CF.$("#bell-count");
  count.textContent = openAlerts.length;
  count.classList.toggle("hidden", openAlerts.length === 0);
  CF.$("#notification-list").innerHTML = openAlerts.length
    ? openAlerts.slice(0, 8).map((alert) => `
        <button class="notification-item link-btn" type="button" data-notification-alerts>
          <strong>${CF.escapeHtml(alert.alert_type)} - ${CF.escapeHtml(alert.severity)}</strong>
          <span>${CF.escapeHtml(alert.message)}</span>
          <small>${CF.fmtDate(alert.created_at)}</small>
        </button>
      `).join("")
    : `<div class="empty">Sin alertas abiertas.</div>`;
  CF.$$("[data-notification-alerts]").forEach((item) => item.addEventListener("click", () => {
    CF.$("#notification-popover").classList.add("hidden");
    CF.navigate("alerts");
  }));
};
