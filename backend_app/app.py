from flask import Flask, send_from_directory, abort
from flask_cors import CORS, cross_origin

# Flask server that hosts an API route for the frontend to hit, which returns metrics
# To start, run the following commands:
# pip install flask
# pip install flask-cors
# python app.py

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["CLIENT_CSV"] = "/app/csv"


@app.route('/')
@cross_origin()
def hello_world():
    return 'This is the index response from the backend'


@app.route('/data')
@cross_origin()
def get_data():
    fname = f"all_data.csv"
    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename=fname, as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
