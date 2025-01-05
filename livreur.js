// Optimisation des trajets
async function optimizeRoute() {
    const response = await fetch(`${API_BASE_URL}/optimize_route`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ traffic_conditions: [[1, 2], [2, 1]] }) // Exemple
    });
    const data = await response.json();
    console.log("Optimized Route:", data);
}

// Ajustement des trajets
async function adjustRoute() {
    const response = await fetch(`${API_BASE_URL}/adjust_route`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ traffic: 2, weather: 1, additional: 1 }) // Exemple
    });
    const data = await response.json();
    console.log("Adjusted Delay:", data);
}
