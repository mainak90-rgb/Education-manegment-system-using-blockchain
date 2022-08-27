from flask import Flask, redirect, url_for
import requests
import json


app = Flask(__name__)
url = "http://127.0.0.1:5050/principal"


@app.route("/")
def hello():
    return "hello"





@app.route("/admin")
class Admin:
    @staticmethod
    def admin():
        return redirect(url_for("/"))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)
