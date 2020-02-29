from app import app, db, mongo
from flask import jsonify








@app.route('/', methods=['GET'])
def index():
    msg = "Welcome!, with this API you can activate or deactivate cards specifying the serial number and category (range) of the card(s) N.B: only assigned cards can be activated!!!, and only activated cards can be deactivated  <<HAPPY TESTING>>!"
    return jsonify({"Message": msg})


