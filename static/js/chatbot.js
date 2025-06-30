document.addEventListener('DOMContentLoaded', function() {
    const chatbotContainer = document.getElementById('chatbot-container');
    const openChatbotBtn = document.getElementById('open-chatbot');
    const toggleChatBtn = document.getElementById('toggle-chat');
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const chatSuggestions = document.getElementById('chat-suggestions');

    // Sugerencias de preguntas frecuentes
    const suggestions = [
        '¿Cuántos RAEE tengo por empresa?',
        '¿Cuántos RAEE tengo por año?',
        '¿Cuál es el impacto ambiental de mis reciclajes?',
        '¿Qué categorías de RAEE existen?',
        '¿Cómo registro un nuevo producto?',
        '¿Cuántas empresas están registradas?',
        '¿Cuáles son los beneficios del reciclaje?'
    ];

    function renderSuggestions() {
        chatSuggestions.innerHTML = '';
        const title = document.createElement('div');
        title.className = 'suggestion-title';
        title.textContent = 'Preguntas sugeridas:';
        chatSuggestions.appendChild(title);
        
        suggestions.forEach(q => {
            const btn = document.createElement('button');
            btn.textContent = q;
            btn.className = 'suggestion-btn';
            btn.onclick = () => {
                chatInput.value = q;
                sendMessage();
            };
            chatSuggestions.appendChild(btn);
        });
        chatSuggestions.style.display = 'block';
        
        // Scroll para mostrar las sugerencias
        setTimeout(() => {
            chatbotContainer.querySelector('#chatbot-body').scrollTop = chatbotContainer.querySelector('#chatbot-body').scrollHeight;
        }, 100);
    }

    function hideSuggestions() {
        chatSuggestions.style.display = 'none';
    }

    openChatbotBtn.onclick = () => {
        chatbotContainer.style.display = 'flex';
        openChatbotBtn.style.display = 'none';
        renderSuggestions();
    };
    toggleChatBtn.onclick = () => {
        chatbotContainer.style.display = 'none';
        openChatbotBtn.style.display = 'block';
    };

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ' + (sender === 'bot' ? 'bot-message' : 'user-message');
        msgDiv.textContent = text;
        chatMessages.appendChild(msgDiv);
        // Scroll en el contenedor principal del chatbot
        chatbotContainer.querySelector('#chatbot-body').scrollTop = chatbotContainer.querySelector('#chatbot-body').scrollHeight;
    }

    async function processMessage(userMessage) {
        try {
            const response = await fetch('/api/chatbot/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: userMessage})
            });
            
            if (response.status === 403) {
                return "❌ Acceso denegado. Solo administradores pueden usar el chatbot.";
            } else if (response.status === 401) {
                return "❌ No autorizado. Debes iniciar sesión.";
            } else if (!response.ok) {
                return "❌ Error del servidor. Intenta de nuevo.";
            }
            
            const data = await response.json();
            return data.response;
        } catch (error) {
            return "Disculpa, hay un problema temporal. Intenta de nuevo.";
        }
    }

    sendBtn.onclick = sendMessage;
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') sendMessage();
    });

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Ocultar sugerencias cuando se envía un mensaje
        hideSuggestions();
        
        appendMessage(message, 'user');
        chatInput.value = '';
        
        const response = await processMessage(message);
        appendMessage(response, 'bot');
        
        // Mostrar sugerencias después de la respuesta
        setTimeout(() => {
            renderSuggestions();
        }, 500);
    }

    // Si el chat está abierto al cargar, mostrar sugerencias
    if (chatbotContainer.style.display !== 'none') {
        renderSuggestions();
    }
}); 