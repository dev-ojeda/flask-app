const socket_io = io("/chat", {
  auth: {
    secret: "f9b949af179c2843e5dc08664d598dc98c76c18ef8c55b2be1469156349bdc95",
  },
  // enable retries
  ackTimeout: 10000,
  retries: 3,
}); // Conecta con el servidor Flask-SocketIO
const chatMessagesDiv = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");
const sendMessageButton = document.getElementById("send-message");
const tblEmpleados = document.getElementById("tblEmpleados");
const toastLiveExample = document.getElementById("liveToast");

// Escucha mensajes del servidor
socket_io.on("receive_message", function (arg) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");
  messageDiv.innerHTML = `<span class="username">${arg.username}:</span> ${arg.message}`;
  chatMessagesDiv.appendChild(messageDiv);
  chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight; // Auto-scroll hacia abajo
});

const message_pag = (message, new_class, tiempo) => {
  debugger;
  const enviado = document.getElementById("datos_message");
  const get_class = enviado.getAttribute("class");
  const set_class = get_class + " " + new_class;
  enviado.setAttribute("class", set_class);
  const nodes = enviado.childNodes[5];
  nodes.innerText = tiempo;
  const contenido = document.getElementById("contenido");
  contenido.innerText = message;
  toastLiveExample.append(contenido);
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
  toastBootstrap.show();
};

// socket_io.on("connect", () => {
//   console.log(socket_io.connected); // true
// });

// socket_io.on("disconnect", () => {
//   console.log(socket_io.disconnect); // false
// });

// Maneja eventos del servidor
socket_io.on("auth_success", (arg) => {
  console.log("Auth Success:", arg.message);
  const auth = JSON.parse(JSON.stringify(arg));
  const message = auth.message;
  const tiempo = auth.enviado;
  const new_class = "bg-success-subtle";
  message_pag(message, new_class, tiempo);
});

socket_io.on("auth_error", (error) => {
  console.error("Auth Error:", error);
  socket.disconnect();
});

// Emitir un evento autenticado

socket_io.on("no_authenticated", (arg) => {
  console.log("Response No Autenticado:", arg);
  const auth = JSON.parse(JSON.stringify(arg));
  const message = auth.message;
  const tiempo = auth.enviado;
  const new_class = "bg-primary-subtle";
  socket_io.emit("authenticated_event", { someData: "example" });
  message_pag(message, new_class, tiempo);
});

socket_io.on("server_message", function (arg) {
  const row_id = JSON.parse(JSON.stringify(arg));
  console.log("DATA", row_id);
  const message = row_id.message + " " + row_id.id;
  const tiempo = row_id.enviado;
  const new_class = "bg-success-subtle";
  message_pag(message, new_class, tiempo);
});

tblEmpleados.addEventListener("click", function (e) {
  seleccion = {};
  if (e.target.classList.contains("select-row")) {
    const row = e.target.closest("tr");
    const id = e.target.getAttribute("data-id");

    // Realiza alguna acción con el ID seleccionado
    console.log("Fila seleccionada con ID:", id);
    seleccion = {
      id: id,
    };
    socket_io.emit("send_queue", JSON.stringify(seleccion));
    // Enviar datos al servidor (opcional)
    fetch("/select-row", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id }),
    })
      .then((response) => response.json())
      .then((data) => console.log("Respuesta del servidor:", data))
      .catch((error) => console.error("Error:", error));
  }
});

sendMessageButton.addEventListener("click", function (e) {
  e.preventDefault();
  const message = chatInput.value.trim();
  const username = "WEB";
  if (username && message) {
    socket_io.emit("send_message", { username: username, message: message });
    chatInput.value = ""; // Limpia el campo de mensaje
  } else {
    alert("Por favor ingresa tu nombre y un mensaje.");
  }
});
