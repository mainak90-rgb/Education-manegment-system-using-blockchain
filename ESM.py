import hashlib
import json
import datetime

# from uuid import uuid4
# from urllib.parse import urlparse

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


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        # self.block = []
        # self.block_size = 3

        self.create_block(proof=1, previous_hash='0')

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

    def is_valid(self, transaction):
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
