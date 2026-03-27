// Initialize the Map (Centering on a generic city coordinate)
const map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Example: Adding a Marker for a "Low Traffic" station
const station = L.marker([51.5, -0.09]).addTo(map)
    .bindPopup('<b>Central Station</b><br>Status: Low Traffic.')
    .openPopup();

// Logic to fetch your ML predictions (Placeholder)
async function getForecast() {
    // const response = await fetch('http://localhost:8000/predict');
    // const data = await response.json();
    console.log("Fetching ARIMA/XGBoost predictions...");
}

getForecast();