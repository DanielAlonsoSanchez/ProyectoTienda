document.addEventListener('DOMContentLoaded', () => {

    // Botón para subir
    const botonSubir = document.querySelector('.boton-subir');
    if (botonSubir) {
        botonSubir.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth', // Esto indica que moverse suave
            });
        });
    }

    // Botón para bajar
    const botonBajar = document.querySelector('.boton-bajar');
    if (botonBajar) {
        botonBajar.addEventListener('click', () => {
            window.scrollTo({
                top: document.body.scrollHeight, // Esto indica que tiene que bajar al tope
                behavior: 'smooth',
            });
        });
    }
});
