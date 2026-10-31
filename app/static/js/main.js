document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const navbar = document.querySelector(".navbar");
  const navToggle = document.getElementById("navbarToggle");
  const navMenu = document.getElementById("navbarMenu");
  const loadingScreen = document.getElementById("loadingScreen");
  const loadingBarFill = document.getElementById("loadingBarFill");
  const loadingPercent = document.getElementById("loadingPercent");
  const loadingRpm = document.getElementById("loadingRpm");
  const loadingLights = document.querySelectorAll(".loading-screen__light");

  /* ---------- Navbar ---------- */
  const handleScroll = () => {
    if (window.scrollY > 50) {
      navbar.classList.add("navbar--scrolled");
    } else {
      navbar.classList.remove("navbar--scrolled");
    }
  };

  window.addEventListener("scroll", handleScroll);

  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("is-open");
    navToggle.classList.toggle("is-active");
    navToggle.setAttribute("aria-expanded", isOpen);
  });

  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("is-open");
      navToggle.classList.remove("is-active");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });

  /* ---------- Animasi masuk hero ---------- */
  const animateHero = () => {
    const hero = document.querySelector(".hero");
    if (!hero) return;

    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    if (prefersReducedMotion) {
      gsap.set(
        [
          ".hero__greeting",
          ".hero__name",
          ".hero__headline",
          ".hero__description",
          ".hero__actions",
          ".hero__socials",
          ".hero__photo",
        ],
        { opacity: 1, y: 0, scale: 1 },
      );
      return;
    }

    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    tl.from(".hero__greeting", { opacity: 0, y: 20, duration: 0.6 })
      .from(".hero__name", { opacity: 0, y: 30, duration: 0.7 }, "-=0.4")
      .from(".hero__headline", { opacity: 0, y: 20, duration: 0.6 }, "-=0.4")
      .from(
        ".hero__description",
        { opacity: 0, y: 20, duration: 0.6 },
        "-=0.35",
      )
      .from(".hero__actions", { opacity: 0, y: 20, duration: 0.6 }, "-=0.35")
      .from(".hero__socials", { opacity: 0, y: 20, duration: 0.6 }, "-=0.35")
      .from(
        ".hero__photo",
        { opacity: 0, scale: 0.85, duration: 0.8 },
        "-=0.6",
      );
  };
  /* ---------- Penjadwal animasi: tunggu sampai layar benar-benar terbuka ---------- */
  const revealCallbacks = [];
  let hasRevealed = false;

  const onReveal = (callback) => {
    if (hasRevealed) {
      callback();
    } else {
      revealCallbacks.push(callback);
    }
  };

  const runReveal = () => {
    hasRevealed = true;
    revealCallbacks.forEach((callback) => callback());
    revealCallbacks.length = 0;
  };

  onReveal(animateHero);

  /* ---------- Loading screen (hanya kunjungan pertama per tab) ---------- */
  const markLoaded = () => {
    try {
      sessionStorage.setItem("msaLoaded", "1");
    } catch (e) {}
  };

  const skipLoading = root.classList.contains("skip-loading");
  const hasTransition = root.classList.contains("has-transition");

  if (loadingScreen && !skipLoading) {
    let progress = 0;

    const interval = setInterval(() => {
      progress += Math.random() * 18 + 7;

      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);

        setTimeout(() => {
          loadingLights.forEach((light) => light.classList.remove("is-lit"));

          setTimeout(() => {
            loadingScreen.classList.add("is-hidden");
            document.body.classList.remove("is-loading");
            markLoaded();
            runReveal();
          }, 200);
        }, 300);
      }

      loadingBarFill.style.width = `${progress}%`;
      loadingPercent.textContent = `${Math.floor(progress)}%`;
      loadingRpm.textContent = `${Math.floor(progress * 90)} RPM`;

      const litCount = Math.floor(progress / 20);
      loadingLights.forEach((light, index) => {
        light.classList.toggle("is-lit", index < litCount);
      });
    }, 150);
  } else {
    document.body.classList.remove("is-loading");

    if (hasTransition) {
      document.addEventListener("pagetransition:reveal", runReveal, {
        once: true,
      });
    } else {
      runReveal();
    }
  }

  /* ---------- Statistik count-up (About) ---------- */
  const statNumbers = document.querySelectorAll(".stat-card__number");

  if (statNumbers.length > 0) {
    const animateCount = (el) => {
      const target = parseInt(el.dataset.target, 10);
      const duration = 1200;
      const startTime = performance.now();

      const step = (now) => {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        el.textContent = Math.floor(progress * target);

        if (progress < 1) {
          requestAnimationFrame(step);
        }
      };

      requestAnimationFrame(step);
    };

    const statsObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            statsObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.6 },
    );

    statNumbers.forEach((el) => statsObserver.observe(el));
  }

  /* ---------- Tilt kartu skill ---------- */
  const skillCards = document.querySelectorAll(".skill-card");
  const supportsHover = window.matchMedia(
    "(hover: hover) and (pointer: fine)",
  ).matches;

  if (supportsHover) {
    skillCards.forEach((card) => {
      const icon = card.querySelector(".skill-card__icon");

      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -6;
        const rotateY = ((x - centerX) / centerX) * 6;

        card.style.transform = `perspective(600px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;

        if (icon) {
          icon.style.transform = `translate(${(x - centerX) / 10}px, ${(y - centerY) / 10}px)`;
        }
      });

      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
        if (icon) {
          icon.style.transform = "";
        }
      });
    });
  }

  /* ---------- Filter proyek + stagger kartu ---------- */
  const filterButtons = document.querySelectorAll(".filter-btn");
  const projectCards = document.querySelectorAll(".project-card");
  const motionAllowed = !window.matchMedia("(prefers-reduced-motion: reduce)")
    .matches;

  if (
    projectCards.length > 0 &&
    motionAllowed &&
    window.gsap &&
    window.ScrollTrigger
  ) {
    gsap.registerPlugin(ScrollTrigger);
    gsap.set(projectCards, { opacity: 0, y: 40 });

    onReveal(() => {
      ScrollTrigger.batch(projectCards, {
        start: "top 90%",
        once: true,
        onEnter: (batch) => {
          gsap.to(batch, {
            opacity: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.12,
            ease: "power2.out",
            overwrite: true,
            clearProps: "transform,opacity",
          });
        },
      });
    });
  }

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterButtons.forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");

      const filter = btn.dataset.filter;
      const visibleCards = [];

      projectCards.forEach((card) => {
        const matches = filter === "All" || card.dataset.category === filter;
        card.style.display = matches ? "" : "none";
        if (matches) visibleCards.push(card);
      });

      if (motionAllowed && window.gsap) {
        gsap.fromTo(
          visibleCards,
          { opacity: 0, y: 20, scale: 0.97 },
          {
            opacity: 1,
            y: 0,
            scale: 1,
            duration: 0.4,
            stagger: 0.07,
            ease: "power2.out",
            overwrite: true,
            clearProps: "transform,opacity",
          },
        );
      }

      if (window.ScrollTrigger) ScrollTrigger.refresh();
    });
  });
  /* ---------- Timeline Journey ---------- */
  const timelineSection = document.getElementById("timeline");

  if (timelineSection && window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);

    const prefersReducedMotionTimeline = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    const timelineFill = document.getElementById("timelineFill");
    const timelineItems = document.querySelectorAll(".timeline__item");

    if (prefersReducedMotionTimeline) {
      if (timelineFill) timelineFill.style.transform = "scaleY(1)";
      timelineItems.forEach((item) => {
        item.style.opacity = 1;
      });
    } else {
      if (timelineFill) {
        gsap.fromTo(
          timelineFill,
          { scaleY: 0 },
          {
            scaleY: 1,
            ease: "none",
            scrollTrigger: {
              trigger: timelineSection,
              start: "top 70%",
              end: "bottom 70%",
              scrub: true,
            },
          },
        );
      }

      timelineItems.forEach((item, index) => {
        const fromLeft = index % 2 === 0;

        gsap.from(item, {
          opacity: 0,
          x: fromLeft ? -40 : 40,
          duration: 0.6,
          ease: "power2.out",
          scrollTrigger: {
            trigger: item,
            start: "top 85%",
            toggleActions: "play none none none",
          },
        });
      });
    }
  }

  /* ---------- Konfirmasi hapus (admin) ---------- */
  document.querySelectorAll(".admin-delete-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      const message = form.dataset.confirm || "Yakin mau menghapus data ini?";

      if (!window.confirm(message)) {
        e.preventDefault();
      }
    });
  });

  /* ---------- Pesan flash menghilang otomatis ---------- */
  document.querySelectorAll(".flash").forEach((el) => {
    setTimeout(() => {
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 300);
    }, 4000);
  });

  /* ---------- Tombol kembali ke atas ---------- */
  const backToTop = document.getElementById("backToTop");

  if (backToTop) {
    window.addEventListener("scroll", () => {
      backToTop.classList.toggle("is-visible", window.scrollY > 400);
    });

    backToTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
  /* ---------- Efek magnetic pada tombol utama ---------- */
  const canUseMagnetic =
    window.matchMedia("(hover: hover) and (pointer: fine)").matches &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (canUseMagnetic && window.gsap) {
    document
      .querySelectorAll(".hero__actions .btn, .navbar__cv")
      .forEach((button) => {
        const moveX = gsap.quickTo(button, "x", {
          duration: 0.4,
          ease: "power3.out",
        });
        const moveY = gsap.quickTo(button, "y", {
          duration: 0.4,
          ease: "power3.out",
        });
        let centerX = 0;
        let centerY = 0;

        button.addEventListener("mouseenter", () => {
          const rect = button.getBoundingClientRect();
          centerX = rect.left + rect.width / 2;
          centerY = rect.top + rect.height / 2;
        });

        button.addEventListener("mousemove", (e) => {
          moveX((e.clientX - centerX) * 0.3);
          moveY((e.clientY - centerY) * 0.3);
        });

        button.addEventListener("mouseleave", () => {
          moveX(0);
          moveY(0);
        });
      });
  }
});
