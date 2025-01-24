document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los botones que abren modales
    var botones = document.querySelectorAll('[data-bs-toggle="modal"]');

    // Iterar sobre cada botón y agregar un evento de clic
    botones.forEach(function(btn) {
        btn.addEventListener('click', function() {

            // Obtener el id del modal que corresponde al botón presionado
            var modalId = btn.getAttribute('data-bs-target');
            var modal = document.querySelector(modalId);

            if (modal) {
                // Mostrar el modal
                modal.style.display = "block";

                // Cerrar el modal si el usuario hace clic fuera del mismo
                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = "none";
                    }
                };
            } else {
                console.error("Modal no encontrado: ", modalId);
            }
        });
    });
});
