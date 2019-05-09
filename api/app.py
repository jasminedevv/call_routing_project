"""WE'RE GROWING TRIES IN MONGO BOIIIIII"""

from flask import Flask, request
from flask_pymongo import PyMongo

from models import lookup_price

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/trie"
mongo = PyMongo(app)

@app.route("/", methods=["GET"])
def find_price():
    """Call like this: url/number=+12345"""
    return lookup_price(request.args.get("number"))