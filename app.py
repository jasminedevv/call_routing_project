from flask import Flask, jsonify

from scenario3 import get_price

app = Flask(__name__)

@app.route("/<number>", methods=["GET"])
def root(number):
  try:
    return jsonify({'price': get_price(bytes(number, 'utf-8'))})
  except KeyError:
    return jsonify({'error': 'Invalid input'})
