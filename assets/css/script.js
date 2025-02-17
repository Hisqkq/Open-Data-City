document.addEventListener("DOMContentLoaded", function () {
    function observeSections() {
        const sections = document.querySelectorAll(".scroll-section");

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        }, { threshold: 0.2 });

        sections.forEach((section) => observer.observe(section));
    }

    // Exécute au chargement initial
    observeSections();

    // Surveille les changements dans le DOM pour ajouter les nouvelles sections
    const observerConfig = { childList: true, subtree: true };
    const mutationObserver = new MutationObserver(() => observeSections());
    mutationObserver.observe(document.body, observerConfig);
});
