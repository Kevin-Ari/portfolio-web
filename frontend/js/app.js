document.getElementById("check-api").addEventListener("click", async () => {
    const res = await fetch("/api/health");
    const data = await res.json();
    document.getElementById("api-status").innerText =
        data.status === "ok" ? "✅ API funcionando correctamente" : "⚠️ Error al conectar";
});
