const socketChat = io("/chat"); // Conecta con el servidor SocketIO en la ns Chat
const form = document.getElementById("chat-form");
const messagesContainer = document.querySelector(".chat-messages");


socketChat.on("connect", () => {
    console.log("Conectado al namespace /chat");
    // Enviar un mensaje al servidor
    const username = "WEB";
    socketChat.emit("mensaje", { "username": username, "msg": "Hola desde el cliente Web" });
});

socketChat.on("disconnect", () => {
    console.log("Desconectado del namespace /chat");
});

// Escucha mensajes del servidor
socketChat.on("respuesta", (data) => {
  // Add user message
  const userMessage = `
  <div class="chat-message user d-flex flex-column align-items-end">
    <div class="message">${data.mensaje}</div>
  </div>`;
  messagesContainer.innerHTML += userMessage;

  // Clear input
  messageInput.value = "";

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
});



form.addEventListener("submit", (e) => {
    e.preventDefault();

    const input = document.getElementById("message-input");
    const messageText = input.value;
    const username = "WEB";
    if (messageText.trim()) {
        // Add user message
        const userMessage = `
        <div class="chat-message user d-flex flex-column align-items-end">
          <div class="message">${messageText}</div>
        </div>`;
        messagesContainer.innerHTML += userMessage;

        socketChat.emit("message_cliente", { "username": username, "msg": messageText });
        // Clear input
        input.value = "";

        // Scroll to the bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});