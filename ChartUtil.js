const { Chart } = require("chart.js")
const csv = require('csv-parser');
const fs = require('fs');

let rawData = []
let headers = [];
let dates = [];

fs.createReadStream('SSLMetricsFakeData.csv')
    .pipe(csv())
    .on('headers', (headersIn) => {
        headers = headersIn;
        console.log(headers);
    })
    .on('data', (row) => {
        console.log(row);
        rawData.push(row);
    })
    .on('end', () => {
        console.log('CSV file successfully processed');
    });

for (var i = 0; i < rawData.length; i++) {
    dates.push(rawData[i]['Date']);
    rawData[i]['Date'] = null;
}


let metrics = [];
for (var i = 1; i < headers.length; i++) {
    metrics[i - 1] = [];
    for (var j = 0; j < rawData.length; j++) {
        metrics[i - 1].push(rawData[j][headers[i]]);
    }
}

headers.shift();

let chartDatasets = [];
for (var i = 0; i < metrics.length; i++) {
    chartDatasets.push({
        label: headers[i],
        data: metrics[i],
        fill: false,
    });
}


var ctx = document.getElementById('main-chart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: dates,
        datasets: chartDatasets
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'SSL Metrics Fake Data'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Date'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
});