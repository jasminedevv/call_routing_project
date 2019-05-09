from flask import Flask, request

mongo = PyMongo(app)

lookup_price(number=""):
    return number

@app.route("/", methods=["GET"])
def find_price():
    """Call like this: url/number=+12345"""
    return lookup_price(request.args.get("number"))