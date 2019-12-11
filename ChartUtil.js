const { Chart } = require("chart.js")
const csv = require('csv-parser');
const fs = require('fs');

let rawData = {}
let headers = [];
let dates = [];

fs.createReadStream('SSLMetricsFakeData.csv')
    .pipe(csv())
    .on('headers', (headersIn) => {
        headers = headersIn;
        console.log(headers);
        for (var i = 0; i < headers.length; i++) {
            rawData[headers[i]] = []
        }
        console.log(rawData);
    })
    .on('data', (row) => {
        console.log(row);
        for (var i = 0; i < headers.length; i++) {
            rawData[headers[i]].push(row[headers[i]])
        }
    })
    .on('end', () => {
        console.log('CSV file successfully processed');
        console.log(rawData);

        dates = rawData['Date'];
        delete rawData['Date'];

        console.log("Dates:");
        console.log(dates);

        let chartDatasets = [];
        for (metric in rawData) {
            chartDatasets.push({
                label: metric,
                data: rawData[metric],
                fill: false,
            });
        }

        console.log("Chart Datasets:")
        console.log(chartDatasets)

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
    });