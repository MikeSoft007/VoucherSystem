from app import app, db, mongo
from flask import jsonify
from app.models import Register, random_digits, twelve_digit_serial_no
# database_serial_no


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "Hello there!": '''Welcome to this route, I AM MICHAEL here with the given priviledges you can activate a Card  
                   or cards with the endpoint (/activate)  and (/deactivate) to deactivate with the given category and 
                    card serial number HAPPY TESTING!'''
    })