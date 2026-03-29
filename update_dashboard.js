async function updateDemo() {
  try {
    // Añadimos Date.now() para que el navegador no use datos viejos en caché
    const response = await fetch("demo_state.json?t=" + Date.now());
    const d = await response.json();

    // ── ACTUALIZACIÓN DE PRODUCCIÓN ──────────────────
    // Usamos los nuevos nombres de campos de tu Python
    document.getElementById("total").textContent = d.real_data.total_feromonas.toLocaleString();
    document.getElementById("nodos").textContent = d.real_data.nodos_conteo;

    // ── ACTUALIZACIÓN DE SANDBOX (EVOLUCIÓN) ──────────
    document.getElementById("sandbox_event").textContent = d.sandbox.evento;
    document.getElementById("sandbox_health").textContent = d.sandbox.salud;
    document.getElementById("sandbox_time").textContent = d.sandbox.tiempo_recuperacion + "s";

    // ── LÓGICA DE COLORES DE SOBERANÍA ───────────────
    const healthEl = document.getElementById("sandbox_health");
    if (d.sandbox.salud === "OK") {
      healthEl.style.color = "#00ff00"; // Verde: Funcionamiento Nominal
    } else if (d.sandbox.salud === "DEGRADED") {
      healthEl.style.color = "#ffff00"; // Amarillo: Latencia detectada
    } else {
      healthEl.style.color = "#ff0000"; // Rojo: Fallo Crítico / Reintentando
    }

  } catch (e) {
    console.log("⚠️ Error en telemetría LBH:", e);
  }
}

// Iniciar el metrónomo de actualización (3 segundos)
setInterval(updateDemo, 3000);
updateDemo();
