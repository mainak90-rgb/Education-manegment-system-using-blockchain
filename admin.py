from flask import Flask
import requests
import json


app = Flask(__name__)
url = "http://127.0.0.1:5050/principal"


@app.route("/admin")
def admin(data):
    requests.post(url, json=json.loads(data))
    return json.loads(data)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)
