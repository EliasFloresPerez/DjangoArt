document.addEventListener("DOMContentLoaded", function () {
    // Mostrar mensajes por 3 segundos
    const mensajes = document.getElementById("mensajes");
    if (mensajes) {
        setTimeout(() => {
            mensajes.style.display = "none";
        }, 3000);
    }

    // ======== MODALES =========
    const abrirModales = document.querySelectorAll("[data-modal]");
    const cerrarModales = document.querySelectorAll(".btn-cerrar-modal");

    abrirModales.forEach(btn => {
        btn.addEventListener("click", function () {
            const modalId = this.getAttribute("data-modal");
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = "block";

                if (modalId === "confirmarEliminacionModal") {
                    const usuarioId = this.getAttribute("data-usuario-id");
                    const usuarioNombre = this.getAttribute("data-usuario-nombre");

                    if (usuarioId && usuarioNombre) {
                        document.getElementById("usuario-id").value = usuarioId;
                        document.getElementById("usuario-nombre").textContent = usuarioNombre;
                    }
                }
            }
        });
    });

    cerrarModales.forEach(btn => {
        btn.addEventListener("click", function () {
            const modal = this.closest(".modal");
            if (modal) {
                modal.style.display = "none";
            }
        });
    });

    window.addEventListener("click", function (e) {
        if (e.target.classList.contains("modal")) {
            e.target.style.display = "none";
        }
    });

    // ======== DATATABLES =========
    if (window.jQuery && $('#tabla-usuarios').length) {
        $('#tabla-usuarios').DataTable({
            language: {
                search: "Buscar:",
                lengthMenu: "Mostrar _MENU_ registros",
                info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
                paginate: {
                    next: "Siguiente",
                    previous: "Anterior"
                },
                zeroRecords: "No se encontraron resultados",
                infoEmpty: "Sin registros disponibles",
                infoFiltered: "(filtrado de _MAX_ registros totales)"
            }
        });
    }
});
