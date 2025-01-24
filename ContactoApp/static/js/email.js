document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.querySelector(".formulario"); // Selecciona el formulario

    if (formulario) {
        formulario.addEventListener("submit", function (e) {
            e.preventDefault(); // Evita que se recargue la página

            // Obtén los datos del formulario
            const formData = new FormData(formulario);

            // Limpia los mensajes previos
            const mensajesContainer = document.querySelector(".messages");
            mensajesContainer.innerHTML = "";

            // Enviar datos al backend usando fetch
            fetch(formulario.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Error en el envío del formulario.");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        mensajesContainer.innerHTML = `
                            <div class="alert alert-success text-center">${data.message}</div>
                        `;
                        formulario.reset(); // Limpia el formulario tras el envío exitoso
                    } else {
                        mensajesContainer.innerHTML = `
                            <div class="alert alert-danger text-center">${data.message}</div>
                        `;
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    mensajesContainer.innerHTML = `
                        <div class="alert alert-danger text-center">Ocurrió un error al enviar el mensaje. Inténtalo nuevamente.</div>
                    `;
                });
        });
    }
});
