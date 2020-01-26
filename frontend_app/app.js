const axios = require("axios");
const fs = require('fs')
const Path = require('path')

var express = require("express");
var app = express();

let data = "Data not yet retrieved from backend";
let indexResponse = "Index response not yet retrieved from backend"
const path = Path.resolve(__dirname, 'all_data.csv')
const writer = fs.createWriteStream(path)
const url = "http://192.168.99.100:5000/"

app.get("/", (req, res, next) => {
    res.send("Hello, Frontend!");
});

app.get("/beindex", (req, res, next) => {
    res.send(indexResponse);
});

app.get("/data", (req, res, next) => {
    res.send("Retrieving data...");
});

async function getData(url) {
    const response = await axios({
        url,
        method: 'GET',
        responseType: 'stream'
    })
    response.data.pipe(writer)
    return new Promise((resolve, reject) => {
        writer.on('finish', resolve)
        writer.on('error', reject)
    })
}

const getIndex = async url => {
    axios.get(url)
        .then((response) => {
            indexResponse = response.data;
            console.log(data);
        }, (error) => {
            console.log(error);
        });
}

app.listen(3000, '0.0.0.0', () => {
    console.log("Server running on port 3000");
    getIndex(url)
    getData(url + 'data');
});