import hashlib
import json
import datetime
import random
import requests
import Db

from flask import Flask, jsonify, request


host_dict = {
    "admin": ["127.0.0.1", "5007"]
}


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        # self.block = []
        # self.block_size = 3

    def create_block(self, proof, previous_hash):
        transaction = self.transactions.pop()
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transaction': transaction
                 }
        # if len(self.block)>0:
        #     self.block.append(bl)
        # else:

        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_valid(self):
        types = Db.find_one(post={"id": id}, collection="Users")
        typer = Db.find_one(post={"id": self.transactions[-1]['receiver']}, collection="Users")
        if types == "Teacher" and typer == "Student":
            return True
        if types == "Principal" and (typer == "Teacher" or typer == "Student"):
            return True
        if types == "Admin":
            return True
        return False

    def add_transaction(self, transaction):
        self.transactions.append(transaction)


miners = set()
blockchain = Blockchain()

app = Flask(__name__)

id = None
host = None
port = None


def select_miner(sender, receiver):
    return random.choice(list(set(host_dict.keys()) - {sender, receiver}))


@app.route("/make_transaction", methods=['POST'])
def make_transaction():
    user = Db.find_one({'id': id}, 'Users')
    if user['user'] == "Student":
        return 'You are not eligible for this request', 400
    json = request.get_json()
    transaction_keys = ['receiver', 'type']
    if not all(key in json for key in transaction_keys):
        return 'Some elements are missing', 400
    json['sender'] = id
    blockchain.add_transaction(json)
    r = {'sender': json["sender"],
         'receiver': json["receiver"],
         'transaction': blockchain.transactions
         }
    requests.post("http://127.0.0.1:5007/get_miner", json=r)

    response = {'Message': f'This transaction will be added to block after verification.'}

    return jsonify(response), 200


@app.route("/get_miner", methods=["GET", "POST"])
def get_miner():
    if id != "admin":
        return "Not eligible", 400
    if request.method == "GET":
        r = {}
        for i, m in enumerate(miners):
            r["miner-" + str(i)] = m

        return jsonify(r), 200

    js = request.get_json()
    mine = select_miner(js["sender"], js["receiver"])
    miners.add(mine)
    print(mine)
    r1 = {'miner': mine,
          'POP': False}
    r = {'chain': blockchain.chain,
         'transaction': js['transaction'],
         'length': len(blockchain.chain)
         }
    requests.post("http://127.0.0.1:5007/update", json={"mine": r1, "chain": r})

    return jsonify(r), 200


@app.route('/get_chain', methods=["GET", "POST"])
def get_chain():
    response = {'chain': blockchain.chain,
                'transaction': blockchain.transactions,
                'length': len(blockchain.chain)
                }
    if request.method == "GET":
        return jsonify(response), 200
    else:
        if id != "admin":
            return "Not eligible", 400
        js = request.get_json()
        requests.post("http://" + js['host'] + ":" + js['port'] + "/add_chain", json=response)
        host_dict[js["id"]] = [js["host"], js["port"]]
        return jsonify(response), 200


@app.route("/mine_block")
def mine_block():
    if not id or id not in miners:
        return 'You are not eligible for this request', 400
    miners.remove(id)
    r1 = {'miner': id,
          'POP': True}
    # for i in host_dict.values():
    #     requests.post("http://" + i[0] + ":" + i[1] + "/miner", json=r)
    if not blockchain.is_valid():
        return jsonify({'Message': f'Last transaction is not valid.'}), 200

    previous_block = blockchain.get_previous_block()

    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congrats, You mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transaction': block['transaction'],}
    r = {'chain': blockchain.chain,
         'length': len(blockchain.chain),
         'transaction': blockchain.transactions
         }
    # for i in host_dict.values():
    #     requests.post("http://" + i[0] + ":" + i[1], json=r)
    requests.post("http://127.0.0.1:5007/update", json={"mine": r1, "chain": r})
    return jsonify(response), 200


@app.route("/update", methods=["POST"])
def update():
    js = request.get_json()
    for i in host_dict.values():
        requests.post("http://" + i[0] + ":" + i[1] + "/miner", json=js['mine'])
        requests.post("http://" + i[0] + ":" + i[1] + "/add_chain", json=js["chain"])


@app.route("/miner", methods=["POST"])
def miner():
    js = request.get_json()
    if js["POP"]:
        miners.remove(js["miner"])
    else:
        miners.add(js["miner"])
    return js


@app.route("/add_chain", methods=["GET", "POST"])
def add_chain():
    if request.method == "GET":
        if id == "admin":
            block = {'index': len(blockchain.chain) + 1,
                     'timestamp': str(datetime.datetime.now()),
                     'proof': 1,
                     'previous_hash': 0,
                     'transaction': blockchain.transactions
                     }
            blockchain.chain.append(block)
            return jsonify(block), 200
        requests.post("http://127.0.0.1:5007/get_chain", json={"id": id, "host": host, "port": port})
        return jsonify({"massage": "Request send"}), 200
    else:
        js = request.get_json()
        blockchain.chain = js["chain"]
        blockchain.transactions = js["transaction"]
        return jsonify(js), 200


@app.route('/register', methods=['POST'])
def register():
    if id != 'admin':
        return "You are not eligible for the request", 400
    js = request.get_json()
    _type = js['type']
    js.pop('type')
    _id = js['id'] if js.get('id') else js['roll']
    if _type == 'Student':
        Db.insert_one(js, 'Student')
    elif _type == 'Teacher':
        Db.insert_one(js, 'Teacher')
    else:
        print("invalid")
        return "Not valid type", 400
    Db.insert_one(post={"id": _id, "user": _type}, collection="Users")
    return "Successfully added to the database", 200


def run(_host, _port, _id):
    global id, host, port
    id = _id
    host = _host
    port = _port
    app.run(host=host, port=port)
