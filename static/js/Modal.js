// Espera que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {

    // ======== MODALES =========
    const abrirModales = document.querySelectorAll("[data-modal]");
    const cerrarModales = document.querySelectorAll(".btn-cerrar-modal");

    // Abrir modal
    abrirModales.forEach(btn => {
        btn.addEventListener("click", function () {
            const modalId = this.getAttribute("data-modal");
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = "block";

                // Si el modal es para eliminar (compartido)
                if (modalId === "confirmarEliminacionModal") {
                    // Para eliminar un usuario
                    const usuarioId = this.getAttribute("data-usuario-id");
                    const usuarioNombre = this.getAttribute("data-usuario-nombre");
                    const nivelId = this.getAttribute("data-nivel-id");
                    const nivelActividad = this.getAttribute("data-nivel-actividad");


                    if (usuarioId && usuarioNombre) {
                        document.getElementById("usuario-id").value = usuarioId;
                        document.getElementById("usuario-nombre").textContent = usuarioNombre;
                    }

                    if (nivelId && nivelActividad) {
                        // Rellenamos el modal con los valores correspondientes
                        document.getElementById("nivel-id").value = nivelId;
                        document.getElementById("nivel-actividad").textContent = nivelActividad;
                    }
                }
            }
        });
    });

    // Cerrar modal
    cerrarModales.forEach(btn => {
        btn.addEventListener("click", function () {
            const modal = this.closest(".modal");
            if (modal) {
                modal.style.display = "none";
            }
        });
    });

    // Cerrar modal al hacer clic fuera
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
