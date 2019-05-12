from flask import Flask, request
import pickle
from trie import Trie


app = Flask(__name__)

TRIE = None
with open('10000000.trie', 'rb') as file:
    print("File opened")
    TRIE = pickle.load(file)

def lookup_price(number=""):
    if number[0] != "+":
        number = "+" + number

    price = TRIE.find_closest(number)
    
    if price is None:
        return "Could not find a price for that number."
    return str(price)

@app.route("/", methods=["GET"])
def find_price():
    """Call like this: url/?number=+12345"""
    return lookup_price(request.args.get("number"))