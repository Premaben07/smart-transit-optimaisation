// The URL where your Python server is running
const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

// Function to get User Status (for User Dashboard)
async function fetchUserStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/user-status`);
        const data = await response.json();
        
        // Update the HTML elements with real data from Python
        document.getElementById('traffic-status').innerText = data.status;
        document.getElementById('traffic-status').style.color = data.color_code;
        console.log("User Data Received:", data);
    } catch (error) {
        console.error("Backend is not responding:", error);
    }
}

// Function to get Model Forecasts (for Admin Dashboard)
async function fetchAdminForecast() {
    try {
        const response = await fetch(`${API_BASE_URL}/forecast`);
        const jsonResponse = await response.json();
        return jsonResponse.data; // This returns the ARIMA, Prophet, and XGBoost lists
    } catch (error) {
        console.error("Failed to fetch forecast data:", error);
    }
}