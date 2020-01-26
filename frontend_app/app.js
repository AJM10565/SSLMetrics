const axios = require("axios");

var express = require("express");
var app = express();

let data = "Data not yet retrieved from backend";
const url = "http://127.0.0.1:5000/"

app.get("/", (req, res, next) => {
    res.send("Hello, Frontend!");
});

app.get("/data", (req, res, next) => {
    res.send(data);
});

const getData = async url => {
    axios.get(url)
        .then((response) => {
            data = response.data;
            console.log(data);
        }, (error) => {
            console.log(error);
        });
}

app.listen(3000, () => {
    console.log("Server running on port 3000");
    getData(url);
});