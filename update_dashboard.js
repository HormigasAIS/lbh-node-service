async function updateDemo() {
  try {
    const response = await fetch("demo_state.json?t=" + Date.now());
    const d = await response.json();

    // ── DATOS BASE ─────────────────────────────
    document.getElementById("total").textContent =
      d.real_data.total_feromonas.toLocaleString();

    document.getElementById("nodos").textContent =
      d.real_data.nodos_conteo;

    // ── SANDBOX ───────────────────────────────
    document.getElementById("sandbox_event").textContent =
      d.sandbox.evento;

    document.getElementById("sandbox_health").textContent =
      d.sandbox.salud;

    document.getElementById("sandbox_time").textContent =
      d.sandbox.tiempo_recuperacion + "s";

    // ── 🧠 NARRADOR LBH (NUEVO) ─────────────────────

    const narrador = document.getElementById("lbh_narrative");

    if (narrador && d.human_readable) {
      const ultima = d.human_readable.ultima_emision;

      narrador.innerHTML = `
        🐜 COLONIA LBH ACTIVA<br><br>
        ${d.human_readable.resumen}<br><br>
        <b>Última emisión:</b><br>
        Nodo: ${ultima.quien}<br>
        Señal: ${ultima.que}<br>
        Tiempo: ${ultima.cuando}<br><br>
        Estado: ${d.human_readable.estado_red}
      `;
    }

  } catch (e) {
    console.log("⚠️ Error en LBH narrador:", e);
  }
}

setInterval(updateDemo, 3000);
updateDemo();
