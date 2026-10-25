document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contactForm");
    if (!form) return;

    const submitBtn = document.getElementById("contactSubmit");
    const btnText = submitBtn.querySelector(".btn__text");
    const icon = submitBtn.querySelector(".btn__icon");
    const originalText = btnText.textContent;
    const originalIconClass = icon.className;

    const showToast = (message, isSuccess) => {
        const toast = document.createElement("div");
        toast.className = `toast toast--${isSuccess ? "success" : "error"}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(() => toast.classList.add("is-visible"));

        setTimeout(() => {
            toast.classList.remove("is-visible");
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    };

    const resetButton = () => {
        submitBtn.disabled = false;
        btnText.textContent = originalText;
        icon.className = originalIconClass;
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        form.querySelectorAll(".form-error").forEach((el) => el.remove());

        submitBtn.disabled = true;
        btnText.textContent = "Mengirim...";
        icon.className = "fa-solid fa-spinner fa-spin btn__icon";

        try {
            const response = await fetch(window.location.href, {
                method: "POST",
                body: new FormData(form),
            });

            const data = await response.json();

            if (data.success) {
                btnText.textContent = "Terkirim";
                icon.className = "fa-solid fa-check btn__icon";
                showToast("Pesanmu berhasil dikirim!", true);
                form.reset();

                setTimeout(resetButton, 2500);
            } else {
                resetButton();

                Object.entries(data.errors || {}).forEach(([field, messages]) => {
                    const input = form.querySelector(`[name="${field}"]`);
                    if (input) {
                        const errorEl = document.createElement("span");
                        errorEl.className = "form-error";
                        errorEl.textContent = messages[0];
                        input.insertAdjacentElement("afterend", errorEl);
                    }
                });

                showToast("Periksa lagi isian formnya ya.", false);
            }
        } catch (err) {
            resetButton();
            showToast("Terjadi kesalahan, coba lagi nanti.", false);
        }
    });
});