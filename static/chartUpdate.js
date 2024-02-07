const ctx = document.getElementById('sensorChart').getContext('2d');
const sensorChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: '온도 (C)',
            data: [],
            borderColor: 'red',
            borderWidth: 1
        }, {
            label: '습도 (%)',
            data: [],
            borderColor: 'blue',
            borderWidth: 1
        }, {
            label: '액화수소 유량 (L/min)',
            data: [],
            borderColor: 'green',
            borderWidth: 1
        }, {
            label: '공기질',
            data: [],
            borderColor: 'purple',
            borderWidth: 1
        }, {
            label: '가스관 압력',
            data: [],
            borderColor: 'orange',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        animation: {
            duration: 2000,
            easing: 'ease-in-out'
        },
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            },
        }
    }
});

async function fetchDataAndUpdateChart() {
    try {
        let data; // 변수를 선언하고 초기화

        const response = await fetch('/data');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        data = await response.json(); // 변수를 초기화
        if (!data) {
            throw new Error('Data is empty or undefined');
        }
        if (!Array.isArray(data)) {
            throw new Error('Data is not an array');
        }

        // 차트 데이터 초기화
        sensorChart.data.labels = [];
        sensorChart.data.datasets.forEach(dataset => {
            dataset.data = [];
        });

        // 데이터 칸 업데이트
        document.getElementById('temperature-box').textContent = `온도: ${data.temperature} °C`;
        document.getElementById('humidity-box').textContent = `습도: ${data.humidity} %`;
        document.getElementById('water-flow-box').textContent = `액화수소 유량: ${data.water_flow} L/min`;
        document.getElementById('air-quality-box').textContent = `공기질: ${data.air_quality_index}`;
        document.getElementById('flex-pressure-box').textContent = `가스관 압력: ${data.flex_pressure}`;

        // 새로운 데이터 추가
        if (Array.isArray(data)) { // 데이터가 배열인지 확인
            data.forEach(d => {
                sensorChart.data.labels.push(d.time);
                d.values.forEach((value, index) => {
                    sensorChart.data.datasets[index].data.push(value);
                });
            });
        }

        // 차트 업데이트
        sensorChart.update();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


// 페이지 로드 시 초기 업데이트 실행
fetchDataAndUpdateChart();

// 10초마다 업데이트 실행
setInterval(fetchDataAndUpdateChart, 10000);