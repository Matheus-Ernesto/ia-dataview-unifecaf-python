async function loadData() {
    try {
        const res = await fetch("data.json");
        const data = await res.json();
        console.log("[INFO] Dados carregados:", data.length);

        // === 1. Gráfico de distribuição de risco ===
        const riskCounts = {};
        data.forEach(d => {
            const risk = d.predicted_risk_label || "Desconhecido";
            riskCounts[risk] = (riskCounts[risk] || 0) + 1;
        });

        new Chart(document.getElementById("riskChart"), {
            type: "pie",
            data: {
                labels: Object.keys(riskCounts),
                datasets: [{
                    data: Object.values(riskCounts),
                    backgroundColor: ["#16a34a", "#facc15", "#dc2626", "#6b7280"],
                }]
            },
            options: { plugins: { legend: { position: "bottom" } } }
        });

        // === 2. Gráfico de distribuição por sexo ===
        const genderCounts = {};
        data.forEach(d => {
            const g = d.gender || "Indefinido";
            genderCounts[g] = (genderCounts[g] || 0) + 1;
        });

        new Chart(document.getElementById("genderChart"), {
            type: "doughnut",
            data: {
                labels: Object.keys(genderCounts),
                datasets: [{
                    data: Object.values(genderCounts),
                    backgroundColor: ["#3b82f6", "#f472b6", "#94a3b8"]
                }]
            },
            options: { plugins: { legend: { position: "bottom" } } }
        });

        // === 3. Gráfico de temperatura média por risco ===
        const tempByRisk = {};
        data.forEach(d => {
            const risk = d.predicted_risk_label || "Desconhecido";
            const t = parseFloat(d.temperature_c) || 0;
            if (!tempByRisk[risk]) tempByRisk[risk] = [];
            tempByRisk[risk].push(t);
        });

        const labels = Object.keys(tempByRisk);
        const avgTemp = labels.map(r => {
            const vals = tempByRisk[r];
            return vals.reduce((a, b) => a + b, 0) / vals.length;
        });

        new Chart(document.getElementById("tempChart"), {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Temperatura Média (°C)",
                    data: avgTemp,
                    backgroundColor: "#60a5fa"
                }]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });

        // === 3. Gráfico de risco por sexo ===
        const genderGroups = { Male: [], Female: [] };

        // separa pacientes por gênero
        data.forEach(d => {
            const gender = (d.gender || "Desconhecido").trim();
            if (genderGroups[gender]) {
                genderGroups[gender].push(d);
            }
        });

        // função que calcula contagem de risco por gênero
        function getRiskCounts(pacientes) {
            const risks = {};
            pacientes.forEach(d => {
                const risk = d.predicted_risk_label || "Desconhecido";
                risks[risk] = (risks[risk] || 0) + 1;
            });
            return risks;
        }

        const maleRiskCounts = getRiskCounts(genderGroups.Male);
        const femaleRiskCounts = getRiskCounts(genderGroups.Female);

        const riskLabels = Array.from(new Set([
            ...Object.keys(maleRiskCounts),
            ...Object.keys(femaleRiskCounts)
        ]));

        const colors = {
            "Baixo": "#22c55e",
            "Médio": "#eab308",
            "Alto": "#ef4444",
            "Desconhecido": "#9ca3af"
        };

        // Paleta de risco (padrão)
        const colors2 = {
            "Baixo": "#22c55e",        // verde
            "Médio": "#eab308",        // amarelo
            "Alto": "#ef4444",         // vermelho
            "Desconhecido": "#9ca3af"  // cinza
        };

        // === gráfico masculino ===
        new Chart(document.getElementById("maleRiskChart"), {
            type: "doughnut",
            data: {
                labels: riskLabels,
                datasets: [{
                    data: riskLabels.map(r => maleRiskCounts[r] || 0),
                    backgroundColor: riskLabels.map(r => colors2[r] || "#60a5fa"), // azul para masculino
                    borderColor: "#1d4ed8",
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: { position: "bottom" },
                    title: {
                        display: true,
                        text: "Distribuição de Risco (Masculino)",
                        color: "#1e3a8a",
                        font: { size: 14, weight: "bold" }
                    }
                }
            }
        });

        // === gráfico feminino ===
        new Chart(document.getElementById("femaleRiskChart"), {
            type: "doughnut",
            data: {
                labels: riskLabels,
                datasets: [{
                    data: riskLabels.map(r => femaleRiskCounts[r] || 0),
                    backgroundColor: riskLabels.map(r => colors2[r] || "#c084fc"), // lilás para feminino
                    borderColor: "#6b21a8",
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: { position: "bottom" },
                    title: {
                        display: true,
                        text: "Distribuição de Risco (Feminino)",
                        color: "#6b21a8",
                        font: { size: 14, weight: "bold" }
                    }
                }
            }
        });

        // === 4. Tabela de dados recentes ===
        const table = document.getElementById("dataTable");
        data.slice(0, 20).forEach(d => {
            const row = `
        <tr class="hover:bg-gray-50">
          <td class="p-2">${d.baby_id}</td>
          <td class="p-2">${d.date}</td>
          <td class="p-2">${d.gender}</td>
          <td class="p-2">${parseFloat(d.temperature_c).toFixed(1)}</td>
          <td class="p-2 font-semibold text-${d.predicted_risk_label === "High" ? "red" : d.predicted_risk_label === "Medium" ? "yellow" : "green"}-600">
            ${d.predicted_risk_label}
          </td>
        </tr>
      `;
            table.insertAdjacentHTML("beforeend", row);
        });

    } catch (err) {
        console.error("[ERRO] Falha ao carregar dados:", err);
    }
}

loadData();
