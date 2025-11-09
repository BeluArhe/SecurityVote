// Espera a que todo el HTML esté cargado
document.addEventListener("DOMContentLoaded", () => {
    
    const registroForm = document.getElementById("registroForm");
    const mensajeDiv = document.getElementById("mensaje");
    
    // Campos de error
    const errorCorreo = document.getElementById("errorCorreo");
    const errorPass = document.getElementById("errorPass");

    registroForm.addEventListener("submit", (event) => {
        // 1. Previene que el formulario se envíe de la forma tradicional
        event.preventDefault();

        // 2. Limpia errores previos
        mensajeDiv.textContent = '';
        mensajeDiv.className = 'mensaje';
        errorCorreo.style.display = 'none';
        errorPass.style.display = 'none';

        // 3. Obtiene los datos del formulario
        const formData = new FormData(registroForm);
        const data = Object.fromEntries(formData.entries());

        // 4. --- Validación de Cliente (RÁPIDA) ---
        let esValido = true;

        if (data.contraseña.length < 8) {
            errorPass.textContent = 'La contraseña debe tener al menos 8 caracteres.';
            errorPass.style.display = 'block';
            esValido = false;
        }

        if (!esCorreoValido(data.correo)) {
            errorCorreo.textContent = 'Por favor, introduce un correo válido.';
            errorCorreo.style.display = 'block';
            esValido = false;
        }
        
        // Si la validación rápida falla, no continuamos
        if (!esValido) {
            return;
        }

        // 5. --- Envío al Backend (Python/Flask) ---
        // (Esto se conecta con tu 'app.py')
        
        // Muestra un loader (opcional)
        const boton = registroForm.querySelector('.btn');
        boton.textContent = 'Registrando...';
        boton.disabled = true;

        fetch('/registro', { // La ruta que definimos en app.py
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Convertimos el objeto JS a un string JSON
            body: JSON.stringify(data), 
        })
        .then(response => response.json()) // Esperamos una respuesta JSON del servidor
        .then(respuestaServidor => {
            
            if (respuestaServidor.status === 'success') {
                // Éxito
                mensajeDiv.textContent = respuestaServidor.message;
                mensajeDiv.className = 'mensaje success';
                registroForm.reset(); // Limpia el formulario
            } else {
                // Error (ej. DNI duplicado)
                mensajeDiv.textContent = respuestaServidor.message;
                mensajeDiv.className = 'mensaje error';
            }
        })
        .catch(error => {
            // Error de red o del servidor
            console.error('Error en fetch:', error);
            mensajeDiv.textContent = 'Error de conexión. Inténtalo de nuevo.';
            mensajeDiv.className = 'mensaje error';
        })
        .finally(() => {
            // Restaura el botón
            boton.textContent = 'Registrarse';
            boton.disabled = false;
        });

    }); // Fin del addEventListener

}); // Fin del DOMContentLoaded


// --- Función de ayuda ---
function esCorreoValido(correo) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(correo).toLowerCase());
}