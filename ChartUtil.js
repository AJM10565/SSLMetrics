const { Chart } = require("chart.js")
const csv = require('csv-parser');
const fs = require('fs');

let rawData = {}
let headers = [];
let dates = [];

// Generate random hexadecimal color
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
// Read in DB
var knex = require("knex")({
    client: "sqlite3",
    connection: {
        filename: "./database/SSLMetrics_historical.db"
    }
})

// Get all rows from master (all metrics compiled) table in DB
let result = knex.from("MASTER").select("*")
result.then(function (rows) {
    // Get all column names in headers array
    headers = Object.keys(rows[0])

    // Initialize an empty array in the rawData object for each metric
    for (var i = 0; i < headers.length; i++) {
        rawData[headers[i]] = []
    }

    // Ppopulate all metrics arrays (effectively columns of the table) one row at a time
    for (var j = 0; j < rows.length; j++) {
        for (var k = 0; k < headers.length; k++) {
            rawData[headers[k]].push(rows[j][headers[k]])
        }
    }

    // Remove dates from rawData object
    dates = rawData['date']
    delete rawData['date']

    console.log("Dates:")
    console.log(dates)
    console.log()
    console.log("Raw Data:")
    console.log(rawData)

    // Create chart dataset object array from rawData
    let chartDatasets = [];
    for (metric in rawData) {
        let randomColor = getRandomColor()
        chartDatasets.push({
            label: metric,
            data: rawData[metric],
            backgroundColor: randomColor,
            borderColor: randomColor,
            fill: false,
        });
    }

    console.log("Chart Datasets:")
    console.log(chartDatasets)

    // Create chart
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
                text: 'SSL Metrics'
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
})

//OLD
// Read in CSV, manipulate data, and create chart from it
/*
fs.createReadStream('all_data.csv')
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
            let randomColor = getRandomColor()
            chartDatasets.push({
                label: metric,
                data: rawData[metric],
                backgroundColor: randomColor,
                borderColor: randomColor,
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
                    text: 'SSL Metrics'
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
*/