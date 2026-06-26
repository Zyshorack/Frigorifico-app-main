document.addEventListener("DOMContentLoaded", loadProducts);

async function loadProducts() {
    const tbody = document.querySelector("#products-table tbody");
    try {
        const response = await fetch("/products");
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const products = await response.json();
        tbody.innerHTML = "";
        products.forEach(product => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${product.id}</td>
                <td>${product.code ?? "-"}</td>
                <td>${product.name}</td>
                <td>${product.description ?? "-"}</td>
                <td>${product.weight ?? "-"} ${product.unit ?? ""}</td>
                <td>
                    ${product.is_active ? "Activo" : "Inactivo"}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch(error) {
        console.error(
            "Error cargando productos:",
            error
        );
        tbody.innerHTML = `
            <tr>
                <td colspan="6">
                    No se pudieron cargar productos
                </td>
            </tr>
        `;
    }
}