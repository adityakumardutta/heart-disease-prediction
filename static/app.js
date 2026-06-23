document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("predictionForm");
    const submitBtn = document.getElementById("submitBtn");
    const spinner = document.getElementById("loadingSpinner");

    if (form && submitBtn && spinner) {
        form.addEventListener("submit", () => {
            submitBtn.disabled = true;
            spinner.classList.remove("d-none");
            const text = submitBtn.querySelector(".submit-text");
            if (text) {
                text.textContent = "Analyzing...";
            }
        });
    }
});
