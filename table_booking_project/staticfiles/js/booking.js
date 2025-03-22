document.addEventListener("DOMContentLoaded", function() {
  const restaurantSelect = document.getElementById("restaurantSelect");
  const tableList = document.getElementById("tableList");
  const selectedTableInput = document.getElementById("selectedTable");
  const bookingDate = document.getElementById("bookingDate");
  const confirmButton = document.getElementById("confirmButton");

  restaurantSelect.addEventListener("change", function() {
      const restaurantId = this.value;

      // Очистка списка столиков
      tableList.innerHTML = '<p class="text-muted">⏳ Загрузка доступных столиков...</p>';
      bookingDate.disabled = true;
      confirmButton.disabled = true;
      selectedTableInput.value = "";

      // Запрос на сервер для получения доступных столиков
      fetch(`/get_available_tables/${restaurantId}/`)
          .then(response => {
              if (!response.ok) {
                  throw new Error("Ошибка при загрузке столиков.");
              }
              return response.json();
          })
          .then(data => {
              tableList.innerHTML = "";

              if (data.tables.length > 0) {
                  data.tables.forEach(table => {
                      const tableButton = document.createElement("button");
                      tableButton.className = "list-group-item list-group-item-action";
                      tableButton.textContent = `Столик №${table.name} (${table.seats} мест)`;
                      tableButton.dataset.tableId = table.id;

                      tableButton.addEventListener("click", function() {
                          document.querySelectorAll(".list-group-item").forEach(btn => btn.classList.remove("active"));
                          this.classList.add("active");
                          selectedTableInput.value = this.dataset.tableId;
                          bookingDate.disabled = false;
                          confirmButton.disabled = false;
                      });

                      tableList.appendChild(tableButton);
                  });
              } else {
                  tableList.innerHTML = '<p class="text-muted">❌ Нет доступных столиков в этом ресторане.</p>';
              }
          })
          .catch(error => {
              console.error("Ошибка:", error);
              tableList.innerHTML = '<p class="text-danger">⚠ Ошибка загрузки столиков. Попробуйте позже.</p>';
          });
  });

  bookingDate.addEventListener("input", function() {
      confirmButton.disabled = !this.value || !selectedTableInput.value;
  });
});
