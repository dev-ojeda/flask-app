// const socketChat = io("/chat"); // Conecta con el servidor Flask-SocketIO
// const chatBody = document.getElementById("chatBody");
// const chatInput = document.getElementById("chatInput");
// const btnSendMessage = document.getElementById("btnSendMessage");
// const tblEmpleados = document.getElementById("tblEmpleados");
// const toastLiveExample = document.getElementById("liveToast");
var document = Document;
var window = Window;
// Configura el tiempo inicial del contador (en segundos)
let countdownTime = parseInt("{{ time_left.total_seconds() }}");
// Función para formatear el tiempo como hh:mm:ss
function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor(seconds % 3600 / 60);
  const secs = seconds % 60;

  return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(
    2,
    "0"
  )}:${String(secs).padStart(2, "0")}`;
}

let resultado = formatTime(countdownTime);
document.getElementById("countdown").textContent = resultado;
// Función para actualizar el contador
function updateCountdown() {
  if (countdownTime > 0) {
    countdownTime -= 1; // Resta 1 segundo
    setTimeout(updateCountdown, 1000); // Llama a la función después de 1 segundo
  } else {
    document.getElementById("countdown").textContent = "La sesión ha expirado.";
    window.location.href = "/logout";
  }
}

// Inicia el contador
updateCountdown();
// // Manejar el evento de cerrar la pestaña o ventana
// window.addEventListener("beforeunload", event => {
//   debugger;
//   console.log(event);
//   const eventData = {
//     event_type: "close",
//     details: "La ventana está a punto de cerrarse"
//   };

//   // Enviar datos al servidor
//   window.navigator.sendBeacon(
//     "http://localhost:5000/handle_event",
//     JSON.stringify(eventData)
//   );

//   // Mostrar un mensaje de confirmación (no todos los navegadores lo mostrarán)
//   event.returnValue = "¿Estás seguro de que deseas salir?";
// });

// Manejar el evento de volver atrás
// window.addEventListener("popstate", event => {
//   debugger;
//   const eventData = {
//     event_type: "back",
//     details: "Se ha hecho clic en el botón de volver"
//   };

//   // Enviar datos al servidor
//   fetch("/handle_event", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify(eventData)
//   })
//     .then(response => response.json())
//     .then(data => {
//       // Mostrar respuesta del servidor
//       console.log(data.message);
//     })
//     .catch(error => console.error("Error:", error));
// });

// Maneja eventos del servidor
// socketChat.on("auth_success", arg => {
//   console.log("Auth Success:", arg.message);
//   const auth = JSON.parse(JSON.stringify(arg));
//   const message = auth.message;
//   const tiempo = auth.enviado;
//   const new_class = "bg-success-subtle";
//   message_pag(message, new_class, tiempo);
// });

// socketChat.on("auth_error", error => {
//   console.error("Auth Error:", error);
//   socket.disconnect();
// });

// // Emitir un evento autenticado

// socketChat.on("no_authenticated", arg => {
//   console.log("Response No Autenticado:", arg);
//   const auth = JSON.parse(JSON.stringify(arg));
//   const message = auth.message;
//   const tiempo = auth.enviado;
//   const new_class = "bg-primary-subtle";
//   socket_io.emit("authenticated_event", { someData: "example" });
//   message_pag(message, new_class, tiempo);
// });

// socketChat.on("server_message", function(arg) {
//   const row_id = JSON.parse(JSON.stringify(arg));
//   console.log("DATA", row_id);
//   const message = row_id.msg + " " + row_id.username;
//   const tiempo = row_id.enviado;
//   const new_class = "bg-success-subtle";
//   message_pag(message, new_class, tiempo);
// });

// tblEmpleados.addEventListener("click", function(e) {
//   seleccion = {};
//   if (e.target.classList.contains("select-row")) {
//     const row = e.target.closest("tr");
//     const id = e.target.getAttribute("data-id");

//     // Realiza alguna acción con el ID seleccionado
//     console.log("Fila seleccionada con ID:", id);
//     seleccion = {
//       id: id
//     };
//     socketChat.emit("send_queue", JSON.stringify(seleccion));
//     // Enviar datos al servidor (opcional)
//     fetch("/select-row", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ id: id })
//     })
//       .then(response => response.json())
//       .then(data => console.log("Respuesta del servidor:", data))
//       .catch(error => console.error("Error:", error));
//   }
// });

// socketChat.on("connect", () => {
//   console.log("Conectado al namespace /chat");
//   // Enviar un mensaje al servidor
//   const username = "WEB";
//   socketChat.emit("message", {
//     username: username,
//     msg: "Cliente Conectado"
//   });
// });

// const message_pag = (message, new_class, tiempo) => {
//   const enviado = document.getElementById("datos_message");
//   const get_class = enviado.getAttribute("class");
//   const set_class = get_class + " " + new_class;
//   enviado.setAttribute("class", set_class);
//   const nodes = enviado.childNodes[5];
//   nodes.innerText = tiempo;
//   const contenido = document.getElementById("contenido");
//   contenido.innerText = message;
//   toastLiveExample.append(contenido);
//   const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
//   toastBootstrap.show();
// };

// // Escucha mensajes del servidor
// // socketChat.on("respuesta", (data) => {
// //   rescibido = JSON.parse(JSON.stringify(data));
// //   // Add user message
// //   const sentMessage = document.createElement("div");
// //   sentMessage.classList.add("message", "sent");
// //   sentMessage.textContent = rescibido.username + " : " + rescibido.msg;
// //   chatBody.appendChild(sentMessage);
// //   // Clear input
// //   chatInput.value = "";
// //   // Scroll to bottom
// //   chatBody.scrollTop = chatBody.scrollHeight;
// // });

// // Escucha mensajes del servidor
// socketChat.on("respuesta", data => {
//   rescibido = JSON.parse(JSON.stringify(data));
//   // Add user message
//   const sentMessage = document.createElement("div");
//   sentMessage.classList.add("message", "sent");
//   sentMessage.textContent = rescibido.username + " : " + rescibido.msg;
//   chatBody.appendChild(sentMessage);
//   // Clear input
//   chatInput.value = "";
//   // Scroll to bottom
//   chatBody.scrollTop = chatBody.scrollHeight;
// });

// socketChat.on("disconnect", data => {
//   console.log("Desconectado del namespace /chat");
//   // Add user message
//   const username = "WEB";
//   const sentMessage = document.createElement("div");
//   sentMessage.classList.add("message", "sent");
//   sentMessage.textContent = data.msg;
//   chatBody.appendChild(sentMessage);
//   socketChat.emit("mensaje", {
//     username: username,
//     msg: "Cliente Desconectado"
//   });
//   // Clear input
//   chatInput.value = "";
//   // Scroll to bottom
//   chatBody.scrollTop = chatBody.scrollHeight;
// });

// btnSendMessage.addEventListener("click", e => {
//   e.preventDefault();
//   const messageText = chatInput.value.trim();
//   const username = "WEB";
//   if (messageText === "") return;

//   // Add sent message
//   const sentMessage = document.createElement("div");
//   sentMessage.classList.add("message", "sent");
//   sentMessage.textContent = messageText;
//   chatBody.appendChild(sentMessage);
//   socketChat.emit("message_cliente", { username: username, msg: messageText });
//   // Clear input
//   chatInput.value = "";

//   // Scroll to the bottom
//   chatBody.scrollTop = chatBody.scrollHeight;
// });

// // Allow sending messages with Enter key
// chatInput.addEventListener("keypress", e => {
//   if (e.key === "Enter") {
//     e.preventDefault();
//     const messageText = chatInput.value.trim();
//     const username = "WEB";
//     if (messageText === "") return;

//     // Add sent message
//     const sentMessage = document.createElement("div");
//     sentMessage.classList.add("message", "sent");
//     sentMessage.textContent = messageText;
//     chatBody.appendChild(sentMessage);
//     socketChat.emit("message_cliente", {
//       username: username,
//       msg: messageText
//     });
//     // Clear input
//     chatInput.value = "";

//     // Scroll to the bottom
//     chatBody.scrollTop = chatBody.scrollHeight;
//   }
// });
