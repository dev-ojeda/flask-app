const socketChat = io("/chat"); // Conecta con el servidor SocketIO en la ns Chat
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');

socketChat.on("connect", () => {
    console.log("Conectado al namespace /chat");
    // Enviar un mensaje al servidor
    const username = "WEB";
    socketChat.emit("mensaje", { "username": username, "msg": "Cliente Conectado" });
});

socketChat.on("disconnect", (data) => {
    console.log("Desconectado del namespace /chat");
    // Add user message
    const username = "WEB";
    const sentMessage = document.createElement('div');
    sentMessage.classList.add('message', 'sent');
    sentMessage.textContent = data.mensaje;
    chatBody.appendChild(sentMessage);
    socketChat.emit("mensaje", { "username": username, "msg": "Cliente Desconectado" });
    // Clear input
    chatInput.value = "";
    // Scroll to bottom
    chatBody.scrollTop = chatBody.scrollHeight;
});

// Escucha mensajes del servidor
socketChat.on("respuesta", (data) => {
    rescibido = JSON.parse(JSON.stringify(data))
    // Add user message
    const sentMessage = document.createElement('div');
    sentMessage.classList.add('message', 'sent');
    sentMessage.textContent = rescibido.username + " : " + rescibido.msg;
    chatBody.appendChild(sentMessage);
    // Clear input
    chatInput.value = "";
    // Scroll to bottom
    chatBody.scrollTop = chatBody.scrollHeight;
});

function sendMessage() {
    const messageText = chatInput.value.trim();
    const username = "WEB";
    if (messageText === '') return;

    // Add sent message
    const sentMessage = document.createElement('div');
    sentMessage.classList.add('message', 'sent');
    sentMessage.textContent = messageText;
    chatBody.appendChild(sentMessage);
    socketChat.emit("message_cliente", { "username": username, "msg": messageText });
    // Clear input
    chatInput.value = '';

    // Scroll to the bottom
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Allow sending messages with Enter key
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});