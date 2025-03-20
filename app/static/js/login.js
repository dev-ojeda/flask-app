var document = Document;
var window = Window;

if (document.readyState !== "loading") {
  console.log("document is already ready, just execute code here");
  console.log(document.readyState);
} else {
  document.addEventListener("DOMContentLoaded", function() {
    console.log("document was not ready, place code here");
    console.log(document.readyState);
    var toastLiveExample = document.getElementById("liveToast");
    var toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
    toastBootstrap.show();
  });
}

// Manejar el evento popstate
window.onpopstate = function(event) {
  console.log(event.state);
  if (event.state) {
    // Cargar el contenido del estado
    loadData(event.state.itemId);
  } else {
    // Contenido inicial si no hay estado
    document.getElementById("content").innerText = "Contenido inicial";
  }
};

const btnToken = document.getElementById("btnToken");
const txtToken = document.getElementById("txtToken");

btnToken.addEventListener("click", async user_id => {
  user_id = "user1";
  const response = await fetch("http://localhost:5000/generate-token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ user_id: user_id })
  });
  const data = await response.json();
  txtToken.value = data.token;
  console.log("Token generado:", data.token);
  return data.token;
});
