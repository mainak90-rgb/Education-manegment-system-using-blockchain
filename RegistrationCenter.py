from flask import Flask, request
from datetime import datetime
import requests

app = Flask(__name__)

host = "127.0.0.1"
port = "5000"
rl = 100
i = 200


@app.route('/registration', methods=['POST'])
def registration():
    js = request.get_json()
    # transaction_keys = ['name', 'email', 'dept', 'mobile', 'type']
    transaction_keys = ['name', 'type']
    if not all(key in js for key in transaction_keys):
        return 'Some elements are missing', 400
    global rl, i
    if js['type'] == 'Student':
        if rl == 199:
            rl = 100
        else:
            rl += 1
        now = datetime.now()
        roll = now.strftime('%d%m%Y%H%M') + str(rl)
        js['roll'] = roll

    if js['type'] == 'Teacher':
        if i == 199:
            i = 100
        else:
            i += 1
        now = datetime.now()
        _id = now.strftime('%d%m%Y%H%M') + str(i)
        js['id'] = _id

    requests.post("http://127.0.0.1:5007/register", json=js)
    return js


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
