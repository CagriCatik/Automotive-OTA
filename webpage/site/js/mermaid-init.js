// webpage/docs/js/mermaid-init.js
window.addEventListener("load", async () => {
    if (!window.mermaid) return;

    mermaid.initialize({ startOnLoad: false });

    // Render any .mermaid blocks that exist in the static HTML
    try {
        await mermaid.run({ querySelector: ".mermaid" });
    } catch (e) {
        // keep silent for PDF builds
    }
});
