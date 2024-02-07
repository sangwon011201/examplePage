const ctx = document.getElementById('sensorChart').getContext('2d');
const sensorChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperature (C)',
            data: [],
            borderColor: 'red',
            borderWidth: 1
        }, {
            label: 'Humidity (%)',
            data: [],
            borderColor: 'blue',
            borderWidth: 1
        }, {
            label: 'Water Flow (L/min)',
            data: [],
            borderColor: 'green',
            borderWidth: 1
        }, {
            label: 'Air Quality Index',
            data: [],
            borderColor: 'purple',
            borderWidth: 1
        }, {
            label: 'Flex Pressure',
            data: [],
            borderColor: 'orange',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();

    // 차트 데이터
    sensorChart.data.labels = data.map(d => d.time);
    sensorChart.data.datasets.forEach((dataset) => {
        switch (dataset.label) {
            case 'Temperature (°C)':
                dataset.data = data.map(d => d.temperature);
                break;
            case 'Humidity (%)':
                dataset.data = data.map(d => d.humidity);
                break;
            case 'Water Flow (L/min)':
                dataset.data = data.map(d => d.water_flow);
                break;
            case 'Air Quality Index':
                dataset.data = data.map(d => d.air_quality_index);
                break;
            case 'Flex Pressure':
                dataset.data = data.map(d => d.flex_pressure);
                break;
        }
    });
    sensorChart.update();

    //데이터 칸 업뎃
    document.getElementById('temperature-box').textContent = `Temperature: ${data[0].temperature} °C`;
    document.getElementById('humidity-box').textContent = `Humidity: ${data[0].humidity} %`;
    document.getElementById('water-flow-box').textContent = `Water Flow: ${data[0].water_flow} L/min`;
    document.getElementById('air-quality-box').textContent = `Air Quality Index: ${data[0].air_quality_index}`;
    document.getElementById('flex-pressure-box').textContent = `Flex Pressure: ${data[0].flex_pressure}`;
}

setInterval(fetchData, 1000); // 10초 간격 업뎃