const ctx = document.getElementById('forecastChart').getContext('2d');

const forecastChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'], // Time steps
        datasets: [
            {
                label: 'Actual Ridership',
                data: [450, 520, 300, 320, 600, 850, 400],
                borderColor: '#2c3e50',
                borderWidth: 3,
                fill: false,
                tension: 0.1
            },
            {
                label: 'ARIMA Forecast',
                data: [440, 500, 310, 330, 580, 800, 410],
                borderColor: '#e67e22', // Orange
                borderDash: [5, 5],
                fill: false
            },
            {
                label: 'Prophet Forecast',
                data: [460, 530, 290, 310, 610, 870, 390],
                borderColor: '#9b59b6', // Purple
                borderDash: [5, 5],
                fill: false
            },
            {
                label: 'XGBoost Forecast',
                data: [452, 518, 302, 322, 595, 845, 405],
                borderColor: '#2ecc71', // Green
                borderWidth: 2,
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'top' }
        },
        scales: {
            y: { beginAtZero: true, title: { display: true, text: 'Passenger Count' } }
        }
    }
});