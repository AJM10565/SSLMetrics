from flask import Flask

# Flask server that hosts an API route for the frontend to hit, which returns metrics

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Metrics!'


if __name__ == '__main__':
    app.run()
