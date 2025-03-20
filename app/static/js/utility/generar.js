// URL de la API Flask
const url = "http://localhost:5000/generate-token";
const mensaje = document.querySelector("#mensaje");
const btnGetToken = document.querySelector("#btnGetToken");
// Función para obtener el token y secreto desde Flask
async function fetchTokenAndSecret() {
  try {
    showSpinner();
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Error al obtener los datos");
    }
    const data = await response.json();
    mensaje.textContent = response.headers.get("Authorization");
    console.log(data);
    hideSpinner();
  } catch (error) {
    console.error("Error:", error);
  }
}

// Llamar a la función
// fetchTokenAndSecret();

function showSpinner() {
  const spinner = document.getElementById("spinner");
  spinner.classList.remove("hidden");
}

// Ocultar spinner
function hideSpinner() {
  const spinner = document.getElementById("spinner");
  spinner.classList.add("hidden");
}

// // Simular una acción con el spinner
// async function simulateAction() {
//   showSpinner();
//   await new Promise(resolve => setTimeout(resolve, 3000)); // Simular una espera de 3 segundos
//   hideSpinner();
// }
