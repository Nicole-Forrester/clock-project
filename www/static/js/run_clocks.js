document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const spinner = document.getElementById("clock-spinner");

    if (form && spinner) {
        form.addEventListener("submit", function () {
            spinner.style.display = "flex"; // show the spinner
        });
    }
});