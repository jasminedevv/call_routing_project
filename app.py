from flask import Flask

from scenario3 import get_price

app = Flask(__name__)

@app.route("/<number>", methods=["GET"])
def root(number):
  return str(get_price(bytes(number, 'utf-8')))
