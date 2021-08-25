"""?"""
import os
import random

import requests
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from flask import Flask, jsonify

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)


@app.route("/")
def route_default():
    """test"""
    return "Welcome to the blockchain"


@app.route("/blockchain")
def route_blockchain():
    """"blockchain"""
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_blockchain_mine():
    """"mine blockchain"""
    transaction_data = "stubbed_transaction_data"
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    return jsonify(block.to_json())


PORT = 8080
ROOT_PORT = PORT

if os.environ.get("PEER") == "True":
    PORT = random.randint(10000, 11000)

    result = requests.get("http://localhost:{}/blockchain".format(ROOT_PORT))
    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        print("\n -- Successfully synchronize the local chain")
    except Exception as error:  # pylint: disable=broad-except
        print("\n -- Error synchronizing : {}".format(error))

app.run(port=PORT)
