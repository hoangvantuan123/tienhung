// static/src/js/performance_chart.js

document.addEventListener('DOMContentLoaded', function() {
    var performanceData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Performance Data',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            data: [65, 59, 80, 81, 56, 55]
        }]
    };

    var ctx = document.getElementById('performanceChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: performanceData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});
