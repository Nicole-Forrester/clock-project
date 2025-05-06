document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const spinner = document.getElementById("clock-spinner");

    if (form && spinner) {
        form.addEventListener("submit", function () {
            spinner.style.display = "flex";
            setTimeout(() => {
                if (document.querySelector(".flash-error")) {
                    spinner.style.display = "none";
                }
            }, 500); // give server time to respond
        });
    }
});