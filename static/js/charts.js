// static/js/charts.js

console.log('📊 Charts JS loaded');

// Helper function to create charts
function createBarChart(elementId, data, title) {
    Plotly.newPlot(elementId, [data], {
        title: title,
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    });
}

function createPieChart(elementId, values, labels) {
    const data = [{
        values: values,
        labels: labels,
        type: 'pie',
        marker: {
            colors: ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
        }
    }];
    
    Plotly.newPlot(elementId, data, {
        paper_bgcolor: 'rgba(0,0,0,0)'
    });
}