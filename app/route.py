from app import app, db, mongo
from flask import jsonify
from app.models import Register, random_digits, twelve_digit_serial_no
# database_serial_no


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "Hello there!": '''Welcome to this route, I AM MICHAEL here with the given priviledges you can activate a Card  with the 
                        endpoint </activate>  and </deactivate> to deactivate a card with the given category happy testing!'''
    })




@app.route('/generate', methods=['GET'])
def generate():
    mongo_data = mongo.db.voucher

    # implemnting while loop to ensure that the random generated pin doesn't already exist in the database
    counter = 1
    while counter >= 1:
        pin = random_digits(15)
        pin1 = mongo_data.find_one({'pin': pin})
        
        if pin1:
            print('again')
            counter = counter + 1
        else:
            print(pin)
            break

    save = Register(pin=str(pin))
    db.session.add(save)
    db.session.commit()
    serial_number = Register.query.filter_by(pin=int(pin)).first()
    pin1 = pin
    sn = twelve_digit_serial_no(serial_number.s_n)
    # sn1 = serial_number.s_n
    # sn = '%012d' % sn1

    # storing to mongo db
    mongo_data.insert({'serial_no': sn, 'pin': pin1, 'activation_status': 0, 'dealer_id': None})

    return jsonify({'serial number': sn, 'PIN': pin1})


# @app.route('/<string:serial_no>', methods=['GET'])
# def check_pin(serial_no):
#     s_n = database_serial_no(serial_no)
#
#     # searching to mongo db
#     mongo_data = mongo.db.pins
#     search = mongo_data.find_one({'serial_no': s_n})
#
#     if search:
#         return jsonify({'message': 'Valid Serial No', 'pin': search['pin']})
#     return jsonify({'message': 'Invalid serial No !!!'})
