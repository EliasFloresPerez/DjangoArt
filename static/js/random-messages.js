// Mensajes aleatorios para el dashboard
const messages = [
    "♻️ Reutiliza, registra, recicla",
    "🌱 Cada RAEE cuenta para el planeta",
    "💡 Registra tus dispositivos electrónicos",
    "🔄 Reduce, reutiliza, recicla RAEE",
    "🌍 Protege el medio ambiente",
    "📱 Recicla tus dispositivos móviles",
    "💻 Dona tus equipos electrónicos",
    "🔋 Gestiona correctamente las baterías",
    "📺 Recicla electrodomésticos viejos",
    "🖥️ Actualiza y recicla computadoras",
    "📞 Reutiliza teléfonos en buen estado",
    "🎮 Recicla consolas de videojuegos",
    "🖨️ Dona impresoras funcionales",
    "🔌 Verifica cables y conectores",
    "📷 Recicla cámaras digitales",
    "🎵 Reutiliza reproductores de música",
    "📺 Dona televisores en buen estado",
    "💾 Recicla discos duros de forma segura",
    "🔋 Gestiona baterías de litio correctamente",
    "🌿 Cada reciclaje ayuda al planeta"
];

function showMessage() {
    const messageElement = document.getElementById('random-message');
    if (messageElement) {
        // Seleccionar mensaje aleatorio
        const randomIndex = Math.floor(Math.random() * messages.length);
        const newMessage = messages[randomIndex];
        
        // Actualizar el mensaje
        const messageText = document.getElementById('message-text');
        if (messageText) {
            messageText.textContent = newMessage;
        }
        
        // Mostrar el aviso
        messageElement.style.display = 'block';
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translate(-50%, -40%)';
        
        // Animar entrada
        setTimeout(() => {
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translate(-50%, -50%)';
        }, 100);
        
        // Ocultar después de 6 segundos
        setTimeout(() => {
            hideMessage();
        }, 6000);
    }
}

function hideMessage() {
    const messageElement = document.getElementById('random-message');
    if (messageElement) {
        // Animar salida
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translate(-50%, -60%)';
        
        // Ocultar después de la animación
        setTimeout(() => {
            messageElement.style.display = 'none';
        }, 500);
    }
}

// Mostrar mensaje cada minuto (120,000 ms)
setInterval(showMessage, 120000);

// Mostrar primer mensaje después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(showMessage, 5000);
});

// Permitir cerrar el aviso haciendo clic
document.addEventListener('DOMContentLoaded', function() {
    const messageElement = document.getElementById('random-message');
    if (messageElement) {
        messageElement.addEventListener('click', hideMessage);
        messageElement.style.cursor = 'pointer';
    }
}); 