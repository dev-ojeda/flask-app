document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("menu-toggle");
    const wrapper = document.getElementById("wrapper");

    toggleButton.addEventListener("click", () => {
        wrapper.classList.toggle("toggled");
    });
});
