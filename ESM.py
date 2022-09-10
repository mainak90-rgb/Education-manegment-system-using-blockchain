import hashlib
import json
import datetime
import random
import requests

from flask import Flask, jsonify, request, redirect, url_for

validity_dict = {
    "t1": ["cse", "Teacher"],
    "t2": ["ee", "Teacher"],
    "t3": ["ece", "Teacher"],
    "s1": ["cse", "Student"],
    "s2": ["ee", "Student"],
    "s3": ["ece", "Student"],
    "pr": ["ece", "Principal"],
    "ad": [None, "Admin"]
}

host_dict = {
    "t1": ["127.0.0.1", "5000"],
    "t2": ["127.0.0.1", "5001"],
    "t3": ["127.0.0.1", "5002"],
    "s1": ["127.0.0.1", "5003"],
    "s2": ["127.0.0.1", "5004"],
    "s3": ["127.0.0.1", "5005"],
    "pr": ["127.0.0.1", "5006"],
    "ad": ["127.0.0.1", "5007"]
}


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        # self.block = []
        # self.block_size = 3

        if id == "ad":
            block = {'index': len(self.chain) + 1,
                     'timestamp': str(datetime.datetime.now()),
                     'proof': 1,
                     'previous_hash': 0,
                     'transaction': self.transactions
                     }
            self.chain.append(block)

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transaction': self.transactions.pop()
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
        transaction = self.transactions[-1]
        if validity_dict[transaction["sender"]][1] == "Student":
            return False
        if validity_dict[transaction["sender"]][1] == "Teacher":
            if validity_dict[transaction["receiver"]][1] != "Student":
                return False
            else:
                if validity_dict[transaction["sender"]][0] == validity_dict[transaction["receiver"]][0]:
                    return True
                else:
                    return False
        if validity_dict[transaction["sender"]][1] == "Teacher":
            if validity_dict[transaction["receiver"]][1] == "Student":
                if validity_dict[transaction["sender"]][0] == validity_dict[transaction["receiver"]][0]:
                    return True
                else:
                    return False
            if validity_dict[transaction["receiver"]][1] == "Teacher":
                return True
        if validity_dict[transaction["sender"]][1] == "Admin":
            return True

    def add_transaction(self, transaction):
        self.transactions.append(transaction)


pos_miners = []
miners = set()
blockchain = Blockchain()

app = Flask(__name__)

id = None


def select_miner():
    return random.choice(pos_miners)


@app.route("/make_transaction", methods=['POST'])
def make_transaction():
    if not id or validity_dict[id][1] == "Student":
        return 'You are not eligible for this request', 400
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements are missing', 400
    blockchain.add_transaction(json)
    miners.add(select_miner())
    response = {'Message': f'This transaction will be added to block after verification.'}
    return jsonify(response), 201


@app.route('/get_chain', methods=["GET", "POST"])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    if request.method == "GET":
        return jsonify(response), 200
    else:
        addr = request.remote_addr
        requests.post(addr, json=response)
        return jsonify(response), 200


@app.route("/mine_block")
def mine_block():
    if not id or validity_dict[id][1] not in miners:
        return 'You are not eligible for this request', 400
    miners.remove(validity_dict[id][1])

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
                'transaction': block['transaction']}
    r ={'chain': block,
        'length': len(blockchain.chain)
        }
    for i in host_dict.values():
        requests.post(i[0]+":"+i[1], json=r)

    return jsonify(response), 200


@app.route("/add_chain", methods=["GET", "POST"])
def add_chain():
    if request.method == "GET":
        requests.post("127.0.0.1:5007")
        return jsonify({"Request send"}), 200
    else:
        js = request.get_json()
        blockchain.chain.append(js["chain"])
        return jsonify(js), 200


def run(host, port, _id):
    global id
    id = _id
    app.run(host=host, port=port)
