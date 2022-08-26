from flask import Flask, request
import requests


app = Flask(__name__)
js = ""


@app.route("/principal", methods=['GET', 'POST'])
def principal():
    global js
    if request.method == "POST":
        js = request.json
    return js


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)
