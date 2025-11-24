const statusEl = document.getElementById('connStatus');
const listEl = document.getElementById('alerts');

const wsUrl = "ws://172.20.10.5:9000/";

// Íconos por nivel
const icons = {
  normal: "✔️",
  advertencia: "⚠️",
  crítico: "🔥"
};

// Contadores
let cTotal = 0, cN = 0, cA = 0, cC = 0;

function updateCounters(nivel) {
  cTotal++;
  if (nivel === "normal") cN++;
  else if (nivel === "advertencia") cA++;
  else if (nivel === "crítico") cC++;

  document.getElementById("countTotal").textContent = cTotal;
  document.getElementById("countNormal").textContent = cN;
  document.getElementById("countAdv").textContent = cA;
  document.getElementById("countCrit").textContent = cC;
}

function addAlert(obj) {
  const li = document.createElement('li');
  li.className = 'alert-item nivel-' + obj.nivel;

  li.innerHTML = `
    <div>
      <strong>${icons[obj.nivel]} ${obj.alerta}</strong>
      <div class="small">${obj.mensaje}</div>
      <div class="meta">
        Sensor: ${obj.sensor_id} — Tipo: ${obj.tipo} — Valor: ${obj.valor}
      </div>
    </div>
    <div style="text-align:right">
      <div class="small">${new Date(obj.timestamp).toLocaleString()}</div>
      <div style="font-weight:bold">${obj.nivel.toUpperCase()}</div>
    </div>
  `;

  // Insertar en la parte superior
  listEl.insertBefore(li, listEl.firstChild);

  // Mantener solo 50 alertas
  while (listEl.childElementCount > 50) {
    listEl.removeChild(listEl.lastChild);
  }
}

function connect() {
  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    statusEl.textContent = "conectado";
  };

  ws.onclose = () => {
    statusEl.textContent = "desconectado";
    setTimeout(connect, 2000);
  };

  ws.onerror = (e) => {
    console.error("WebSocket error", e);
    ws.close();
  };

  ws.onmessage = (ev) => {
    try {
      const obj = JSON.parse(ev.data);
      updateCounters(obj.nivel);
      addAlert(obj);
    } catch (e) {
      console.error("Mensaje inválido", e);
    }
  };
}

connect();
