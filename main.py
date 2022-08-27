from flask import Flask, request, abort
import requests


app = Flask(__name__)

host = '127.0.0.1'
port = 80
URL = "http://" + host + ":" + str(port)
# transaction = []


class Admin:
    id = "admin"
    transaction = []

    @staticmethod
    def set_transaction(t):
        Admin.transaction.append(t)

    @staticmethod
    def get_transaction():
        return Admin.transaction


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        data = request.get_json()
        if data['rid'] == Admin.id:
            Admin.set_transaction(data)
            return f"Transaction successful.\n{data['sid']} --> {data['data']}"
        requests.post(URL+"/"+data['rid'], json=request.json)
        return request.json
    else:
        if Admin.transaction:
            return Admin.transaction
        return "No transaction."


class Principal:
    id = "principal"
    transaction = Admin.get_transaction()

    @staticmethod
    def get_last_transaction():
        for i in range(len(Principal.transaction)-1, -1, -1):
            if Principal.transaction[i]["rid"] == "principal":
                return Principal.transaction[i]
        return "No previous transaction"

    def get_last_initiated_transaction(self):
        for i in range(len(self.transaction)-1, -1, -1):
            if self.transaction[i]["sid"] == "principal":
                return self.transaction[i]
        return "No previous transaction"


@app.route("/principal", methods=['GET', 'POST'])
def principal():
    if request.method == "POST":
        data = request.get_json()
        if data['sid'] == Principal.id:
            requests.post(URL+"/admin", json=request.json)
            return request.json
        elif data['rid'] == "principal":
            Admin.set_transaction(data)
            return f"Transaction successful.\n{data['sid']} --> {data['data']}"
        else:
            abort(400)
    else:
        return Principal.get_last_transaction()


class Teacher:
    transaction = Admin.get_transaction()
    id = None

    def __init__(self, _id):
        self.id = _id

    def get_last_transaction(self):
        for i in range(len(self.transaction)-1, -1, -1):
            if self.transaction[i]["rid"] == self.id:
                return self.transaction[i]
        return "No previous transaction"

    def get_last_initiated_transaction(self):
        for i in range(len(self.transaction)-1, -1, -1):
            if self.transaction[i]["sid"] == self.id:
                return self.transaction[i]
        return "No previous transaction"


@app.route("/teacher1", methods=['GET', 'POST'])
def teacher1():
    t1 = Teacher("teacher1")
    if request.method == "POST":
        data = request.get_json()
        if data['sid'] == t1.id:
            requests.post(URL+"/admin", json=request.json)
            return request.json
        elif data['rid'] == t1.id:
            Admin.set_transaction(data)
            return f"Transaction successful.\n{data['sid']} --> {data['data']}"
        else:
            abort(400)
    else:
        return t1.get_last_transaction()


@app.route("/teacher2", methods=['GET', 'POST'])
def teacher2():
    t2 = Teacher("teacher2")
    if request.method == "POST":
        data = request.get_json()
        if data['sid'] == t2.id:
            requests.post(URL+"/admin", json=request.json)
            return request.json
        elif data['rid'] == t2.id:
            Admin.set_transaction(data)
            return f"Transaction successful.\n{data['sid']} --> {data['data']}"
        else:
            abort(400)
    else:
        return t2.get_last_transaction()


@app.route("/teacher3", methods=['GET', 'POST'])
def teacher3():
    t3 = Teacher("teacher3")
    if request.method == "POST":
        data = request.get_json()
        if data['sid'] == t3.id:
            requests.post(URL+"/admin", json=request.json)
            return request.json
        elif data['rid'] == t3.id:
            Admin.set_transaction(data)
            return f"Transaction successful.\n{data['sid']} --> {data['data']}"
        else:
            abort(400)
    else:
        return t3.get_last_transaction()


if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
