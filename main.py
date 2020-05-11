from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "FAST!!!!"


if __name__ == '__main__':
    app.run(host='127.0.0.7', port=8080)
