document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("pageTransition");
    if (!overlay || !window.gsap) return;

    const root = document.documentElement;
    const panelRed = overlay.querySelector(".page-transition__panel--red");
    const panelBlack = overlay.querySelector(".page-transition__panel--black");
    const label = document.getElementById("pageTransitionLabel");
    const main = document.querySelector("main");
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const isAdminPage = window.location.pathname.startsWith("/admin");

    let isLeaving = false;

    const readFlag = () => {
        try { return sessionStorage.getItem("msaTransition"); } catch (e) { return null; }
    };
    const writeFlag = (value) => {
        try { sessionStorage.setItem("msaTransition", value); } catch (e) {}
    };
    const clearFlag = () => {
        try { sessionStorage.removeItem("msaTransition"); } catch (e) {}
    };

    const getPageLabel = (href) => {
        const path = new URL(href, window.location.origin).pathname;
        if (path === "/") return "Home";
        const lastPart = path.split("/").filter(Boolean).pop();
        return lastPart.replace(/-/g, " ");
    };

    const resetOverlay = () => {
        gsap.killTweensOf([panelRed, panelBlack, label, main]);
        root.classList.remove("has-transition");
        overlay.style.visibility = "";
        gsap.set([panelRed, panelBlack, label, main], { clearProps: "all" });
        isLeaving = false;
    };

    // Halaman baru: layar sudah tertutup panel, lalu panel menyapu keluar
    const enter = (pageLabel) => {
        label.textContent = pageLabel;
        gsap.set([panelRed, panelBlack], { skewX: -15, xPercent: 0 });

        gsap.timeline({ onComplete: resetOverlay })
            .to(label, { opacity: 0, duration: 0.25, ease: "power1.out" }, 0.15)
            .call(() => document.dispatchEvent(new CustomEvent("pagetransition:reveal")), null, 0.3)
            .to(panelBlack, { xPercent: 100, duration: 0.5, ease: "power3.inOut" }, 0.2)
            .to(panelRed, { xPercent: 100, duration: 0.5, ease: "power3.inOut" }, 0.3)
            .from(main, { opacity: 0, y: 24, duration: 0.45, ease: "power2.out" }, 0.35);
    };

    // Halaman lama: panel menyapu masuk menutup layar, lalu pindah halaman
    const leave = (href) => {
        if (isLeaving) return;
        isLeaving = true;

        const pageLabel = getPageLabel(href);
        label.textContent = pageLabel;
        writeFlag(pageLabel);

        overlay.style.visibility = "visible";
        gsap.set([panelRed, panelBlack], { skewX: -15, xPercent: -100 });
        gsap.set(label, { opacity: 0 });

        gsap.timeline({
            onComplete: () => {
                window.location.href = href;
            },
        })
            .to(main, { opacity: 0, duration: 0.3, ease: "power1.in" }, 0)
            .to(panelRed, { xPercent: 0, duration: 0.45, ease: "power3.inOut" }, 0)
            .to(panelBlack, { xPercent: 0, duration: 0.45, ease: "power3.inOut" }, 0.1)
            .to(label, { opacity: 1, duration: 0.2 }, 0.4);
    };

    document.addEventListener("click", (e) => {
        if (prefersReducedMotion || isAdminPage || e.defaultPrevented) return;
        if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        const link = e.target.closest("a");
        if (!link) return;
        if (link.target && link.target !== "_self") return;
        if (link.hasAttribute("download")) return;

        const rawHref = link.getAttribute("href");
        if (!rawHref || rawHref.startsWith("#") || rawHref.startsWith("mailto:") || rawHref.startsWith("tel:")) return;

        const url = new URL(link.href, window.location.href);
        if (url.origin !== window.location.origin) return;
        if (url.pathname.startsWith("/admin") || url.pathname.startsWith("/static")) return;

        if (url.pathname === window.location.pathname && url.search === window.location.search) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
            return;
        }

        e.preventDefault();
        leave(url.href);
    });

    // Tombol Back/Forward: browser kadang memulihkan halaman dari memori, bersihkan overlay-nya
    window.addEventListener("pageshow", (event) => {
        if (event.persisted) {
            resetOverlay();
            clearFlag();
        }
    });

    const storedLabel = readFlag();
    clearFlag();

    if (root.classList.contains("has-transition") && storedLabel) {
        enter(storedLabel);
    } else {
        root.classList.remove("has-transition");
    }
});