from flask import Flask, redirect, url_for, request, abort

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return "Hello World !!!"
    else:
        return "No Hello World !!!"


@app.route('/user')
def user():
    return redirect(url_for('hello'))


app.run()
