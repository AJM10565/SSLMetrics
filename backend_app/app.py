from flask import Flask
from flask_cors import CORS, cross_origin

# Flask server that hosts an API route for the frontend to hit, which returns metrics
# To start, run the following commands:
# pip install flask
# pip install flask-cors
# python app.py

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello_world():
    return 'This is the response from the backend'


if __name__ == '__main__':
    app.run()
