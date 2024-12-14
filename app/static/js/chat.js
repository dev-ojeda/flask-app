const socketChat = io("/chat"); // Conecta con el servidor SocketIO en la ns Chat
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatMessages = document.getElementById("chat-messages");

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const messageText = messageInput.value.trim();
  const username = "WEB";
  if (username && messageText) {
    socketChat.emit("message_cliente", { "username": username, "msg": messageText });
    messageInput.value = ""; // Limpia el campo de mensaje
  } else {
    alert("Por favor ingresa tu nombre y un mensaje.");
  }
});

socketChat.on("connect", () => {
  console.log("Conectado al namespace /chat");
  // Enviar un mensaje al servidor
  const username = "WEB";
  socketChat.emit("mensaje", { "username": username, "msg": "Hola desde el cliente Web" });
});

// Recibir respuesta del servidor
// socketChat.on("respuesta", (data) => {
//   debugger;
//   console.log(`Respuesta del servidor: ${data.mensaje}`);
// });

socketChat.on("disconnect", () => {
  console.log("Desconectado del namespace /chat");
});

// Escucha mensajes del servidor
socketChat.on("respuesta", (data) => {
  // Add user message
  const userMessage = document.createElement("div");
  userMessage.className = "d-flex justify-content-end mb-3";
  userMessage.innerHTML = `<div class="p-3 bg-primary text-white rounded">${data.mensaje}</div>`;
  chatMessages.appendChild(userMessage);

  // Clear input
  messageInput.value = "";

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
});

// Escucha mensajes del servidor
socketChat.on("receive_message", (data) => {
  const userMessage = document.createElement("div");
  userMessage.className = "d-flex justify-content-end mb-3";
  userMessage.innerHTML = `<div class="p-3 bg-primary text-white rounded">${data.mensaje}</div>`;
  chatMessages.appendChild(userMessage);

  // Clear input
  messageInput.value = "";

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
});