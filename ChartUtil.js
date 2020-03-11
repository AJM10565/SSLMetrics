const { Chart } = require("chart.js")
const csv = require('csv-parser');
const fs = require('fs');
//Chart.defaults.global.elements.point.pointStyle = 'star';
//plot(sin(1,10), "steppedLine=after&backgroundColor=transparent&borderColor=gray&borderWidth=2&label=Step Function")

let rawData = {}
let headers = [];
let dates = [];

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

fs.createReadStream('SSLMetrics_historical.db')
    .pipe(indexedDB())
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
            let randomColor = getRandomColor()
            chartDatasets.push({
                label: metric,
                data: rawData[metric],
                backgroundColor: randomColor,
                borderColor: randomColor,
                //borderDash: [10, 5],
                pointStyle: 'star',
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